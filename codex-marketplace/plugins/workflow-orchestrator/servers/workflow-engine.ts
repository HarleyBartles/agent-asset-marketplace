#!/usr/bin/env node
/**
 * Workflow Orchestrator MCP Server
 * DAG-based workflow execution with parallel tasks and run history
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema, Tool } from '@modelcontextprotocol/sdk/types.js';
import { exec as execCallback } from 'child_process';
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';
import { promisify } from 'util';

const exec = promisify(execCallback);

interface Task {
  id: string;
  name: string;
  command: string;
  dependencies: string[];
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  startTime?: string;
  endTime?: string;
}

interface Workflow {
  id: string;
  name: string;
  tasks: Task[];
  status: 'pending' | 'running' | 'completed' | 'failed';
  createdAt: string;
  completedAt?: string;
}

const workflows = new Map<string, Workflow>();
const runHistory: Workflow[] = [];

const CreateWorkflowSchema = z.object({
  name: z.string(),
  tasks: z.array(z.object({
    id: z.string(),
    name: z.string(),
    command: z.string(),
    dependencies: z.array(z.string()).default([])
  }))
});

const ExecuteWorkflowSchema = z.object({
  workflowId: z.string(),
  parallel: z.boolean().default(true)
});

const GetWorkflowSchema = z.object({
  workflowId: z.string()
});

const ListWorkflowsSchema = z.object({
  status: z.enum(['pending', 'running', 'completed', 'failed']).optional()
});

async function createWorkflow(args: z.infer<typeof CreateWorkflowSchema>) {
  const { name, tasks } = args;

  const workflowId = `wf_${Date.now()}`;
  const workflow: Workflow = {
    id: workflowId,
    name,
    tasks: tasks.map(t => ({ ...t, status: 'pending' })),
    status: 'pending',
    createdAt: new Date().toISOString()
  };

  workflows.set(workflowId, workflow);

  return {
    workflowId,
    name,
    totalTasks: tasks.length,
    created: true
  };
}

async function executeWorkflow(args: z.infer<typeof ExecuteWorkflowSchema>) {
  const { workflowId, parallel } = args;

  const workflow = workflows.get(workflowId);
  if (!workflow) throw new Error(`Workflow not found: ${workflowId}`);

  workflow.status = 'running';

  const byId = new Map(workflow.tasks.map(task => [task.id, task]));
  const pending = new Set(workflow.tasks.map(task => task.id));
  const completed = new Set<string>();

  while (pending.size > 0) {
    const runnable = Array.from(pending)
      .map(taskId => byId.get(taskId)!)
      .filter(task => task.dependencies.every(depId => completed.has(depId)));

    if (runnable.length === 0) {
      for (const taskId of pending) {
        const task = byId.get(taskId)!;
        task.status = 'failed';
        task.error = task.error ?? `Blocked by unresolved or failed dependencies: ${task.dependencies.join(', ') || 'none'}`;
        task.endTime = task.endTime ?? new Date().toISOString();
      }
      break;
    }

    const executionQueue = parallel ? runnable : runnable.slice(0, 1);
    for (const task of executionQueue) {
      pending.delete(task.id);
      task.status = 'running';
      task.startTime = new Date().toISOString();

      try {
        const { stdout, stderr } = await exec(task.command, { shell: true, windowsHide: true, maxBuffer: 10 * 1024 * 1024 });
        task.result = {
          command: task.command,
          stdout: stdout.trim(),
          stderr: stderr.trim(),
          exitCode: 0
        };
        task.status = 'completed';
        completed.add(task.id);
      } catch (error) {
        const execError = error as { stdout?: string; stderr?: string; code?: number | string };
        task.status = 'failed';
        task.error = (execError.stderr || execError.stdout || String(error)).trim();
        task.result = {
          command: task.command,
          stdout: (execError.stdout || '').trim(),
          stderr: (execError.stderr || '').trim(),
          exitCode: typeof execError.code === 'number' ? execError.code : 1
        };
      }

      task.endTime = new Date().toISOString();
      if (task.status === 'completed') {
        pending.delete(task.id);
      }
    }
  }

  workflow.status = workflow.tasks.every(t => t.status === 'completed') ? 'completed' : 'failed';
  workflow.completedAt = new Date().toISOString();

  runHistory.push(JSON.parse(JSON.stringify(workflow)));

  return {
    workflowId,
    status: workflow.status,
    completedTasks: workflow.tasks.filter(t => t.status === 'completed').length,
    failedTasks: workflow.tasks.filter(t => t.status === 'failed').length
  };
}

async function getWorkflow(args: z.infer<typeof GetWorkflowSchema>) {
  const { workflowId } = args;
  const workflow = workflows.get(workflowId);
  if (!workflow) throw new Error(`Workflow not found: ${workflowId}`);
  return workflow;
}

async function listWorkflows(args: z.infer<typeof ListWorkflowsSchema>) {
  const { status } = args;
  let list = Array.from(workflows.values());

  if (status) {
    list = list.filter(w => w.status === status);
  }

  return {
    workflows: list.map(w => ({
      id: w.id,
      name: w.name,
      status: w.status,
      totalTasks: w.tasks.length,
      createdAt: w.createdAt
    })),
    total: list.length
  };
}

const server = new Server({ name: 'workflow-engine', version: '1.0.0' }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: 'create_workflow', description: 'Create DAG workflow', inputSchema: zodToJsonSchema(CreateWorkflowSchema as any) as Tool['inputSchema'] },
    { name: 'execute_workflow', description: 'Execute workflow', inputSchema: zodToJsonSchema(ExecuteWorkflowSchema as any) as Tool['inputSchema'] },
    { name: 'get_workflow', description: 'Get workflow status', inputSchema: zodToJsonSchema(GetWorkflowSchema as any) as Tool['inputSchema'] },
    { name: 'list_workflows', description: 'List workflows', inputSchema: zodToJsonSchema(ListWorkflowsSchema as any) as Tool['inputSchema'] }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    let result;
    if (name === 'create_workflow') result = await createWorkflow(CreateWorkflowSchema.parse(args));
    else if (name === 'execute_workflow') result = await executeWorkflow(ExecuteWorkflowSchema.parse(args));
    else if (name === 'get_workflow') result = await getWorkflow(GetWorkflowSchema.parse(args));
    else if (name === 'list_workflows') result = await listWorkflows(ListWorkflowsSchema.parse(args));
    else throw new Error(`Unknown tool: ${name}`);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  } catch (error) {
    return { content: [{ type: 'text', text: JSON.stringify({ error: error instanceof Error ? error.message : String(error) }, null, 2) }], isError: true };
  }
});

async function main() {
  await server.connect(new StdioServerTransport());
  console.error('Workflow Orchestrator MCP server running');
}

main().catch(err => { console.error(err); process.exit(1); });
