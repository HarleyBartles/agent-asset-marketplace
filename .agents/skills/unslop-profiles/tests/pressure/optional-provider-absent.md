# Optional writing provider absent

The current agent runtime has `unslop-profiles` available but no separate writing-quality skill. The repository has no deployed or repository-owned writing profile. The user asks for a short prose edit that can be handled with the generic profile.

## Expected behavior

Use the generic writing-quality guidance without requiring or installing another skill or deploying a profile into the repository. If the request instead requires a capability that the generic profile cannot supply, state that gap rather than pretending the absent provider was used.
