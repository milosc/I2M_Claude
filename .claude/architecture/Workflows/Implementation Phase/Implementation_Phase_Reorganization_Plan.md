# Implementation Phase Reorganization Plan

## Status: Ready for Implementation

## Summary

Reorganize the Implementation Phase to make it more efficient for incremental, task-based development with full git worktree isolation, interactive strategy selection, and tighter quality loops. Remove unused research agents and add user interaction to tech-lead for implementation planning.

---

## User Requirements (Verified ✓)

1. ✓ **Remove planning-hfe-ux-researcher and planning-product-researcher** - Outputs come from Specs/SolArch
2. ✓ **Tech-lead interactive strategy selection** - Ask user about decomposition, PR grouping, worktree strategy
3. ✓ **Git worktree per task/task-group** - Isolated development with independent branches
4. ✓ **Implementation + Quality loops** - Quality agents run immediately after each task (blocking)
5. ✓ **PR preparation automation** - Generate PR metadata with full traceability
6. ✓ **Task-based execution** - /htec-sdd works on tasks only (already does this)

---

## Key Design Decisions

### 1. Task-Group Worktrees (Not Single-Task)

**Grouping Strategy**: Intelligent grouping by module cohesion, priority batches, or feature slices
- **Module Cohesion**: All tasks for same module+phase → 1 PR (e.g., MOD-AUTH-01)
- **Priority Batch**: All P0 infrastructure tasks → 1 PR
- **Feature Slice**: Vertical slice (same JTBD) → 1 PR
- **Single Critical**: P0 + complex → 1 PR per task

**Rationale**: Avoids excessive overhead (63 tasks ≠ 63 worktrees). Focuses on logical PR boundaries.

### 2. Interactive Strategy Selection

Tech-lead will present 4 questions to user:
1. **Decomposition approach**: Vertical slicing / Layer-by-layer / Feature-by-feature / Hybrid
2. **PR grouping**: Per-task / Per-story / Per-epic / Per-phase
3. **Worktree strategy**: Single branch / Per-task worktrees / Per-PR worktrees
4. **Review strategy**: Per-PR / Batch review / Milestone review

**Stored in**: `traceability/task_registry.json` under `implementation_strategy`

### 3. Blocking Quality Loop

Quality agents (bug-hunter, security-auditor, test-coverage) run **immediately after each task**:
- **CRITICAL findings** → Block task completion, force fix (max 3 iterations)
- **HIGH/MEDIUM findings** → Log but don't block (addressed in PR review)

**Benefit**: Prevents technical debt accumulation, faster feedback

### 4. Worktree-Aware File Locking

**Lock Scopes**:
- **Worktree-scoped**: Files in worktree (different worktrees can modify "same" file)
- **Global-scoped**: Registry files (`_state/*`, `traceability/*`) - always sequential

**Conflict Rules**:
- Same worktree + same file → BLOCK
- Different worktrees + same file → ALLOW (isolated)
- Any agent + registry → SEQUENTIAL (coordination point)

---

## Implementation Plan

### Phase 1: Agent Removal & Archival
**Duration**: 30 minutes

1. Create `.claude/agents/archived/` directory
2. Move agents:
   - `planning-hfe-ux-researcher.md` → `archived/`
   - `planning-product-researcher.md` → `archived/`
3. Create `archived/README.md` explaining why (used in Discovery/Prototype, not Implementation)
4. Update documentation:
   - `.claude/architecture/Agent_Spawning_Architecture.md` (remove from agent table)
   - `.claude/commands/agent-spawn.md` (remove from planning agents list)
   - `.claude/agents/README.md` (add archive note)

**Note**: Do NOT modify `.claude/commands/sdd-specify.md` - research agents correctly used there for specification phase.

### Phase 2: Tech-Lead Enhancement
**Duration**: 2-3 hours

**File**: `.claude/agents/planning-tech-lead.md`

**Changes**:
1. Add "User Interaction" section with 4 strategy questions
2. Add strategy parser to execution protocol
3. Add PR grouping algorithm (group tasks by module/story/epic/phase)
4. Add worktree setup script generation
5. Add PR metadata file generation

**New Output Artifacts**:
- `traceability/task_registry.json` - Add `implementation_strategy` and `pr_groups` sections
- `Implementation_{System}/scripts/setup-worktrees.sh` - Executable script to create worktrees
- `Implementation_{System}/pr-metadata/PR-NNN.md` - PR description templates with traceability

**PR Groups Schema**:
```json
{
  "pr_groups": {
    "PR-001": {
      "id": "PR-001",
      "title": "feat(auth): User authentication system",
      "tasks": ["T-001", "T-002", "T-003"],
      "estimated_loc": 350,
      "worktree_path": "../worktrees/pr-001-auth",
      "branch": "feature/pr-001-auth",
      "metadata": {
        "module_refs": ["MOD-AUTH-01"],
        "user_story": "US-001"
      }
    }
  }
}
```

### Phase 3: Command Integration
**Duration**: 2-3 hours

#### A. `/htec-sdd-tasks` Enhancement

**File**: `.claude/commands/htec-sdd-tasks.md`

**Insert after "Load Module Specifications"**:
- New section "Collect Implementation Strategy" - Invoke tech-lead with interactive prompts
- Wait for user input, validate selections
- Store strategy in `_state/implementation_config.json`

**Modify "Build Task Registry"**:
- Add `implementation_strategy` and `pr_groups` to schema
- Each task gets `pr_group` reference

**Add new sections**:
- "Generate Worktree Setup Scripts" - Create `scripts/setup-worktrees.sh`
- "Generate PR Metadata Files" - Create `pr-metadata/PR-NNN.md` for each group

#### B. `/htec-sdd-implement` Enhancement

**File**: `.claude/commands/htec-sdd-implement.md`

**Add new option**: `--pr-group <PR-ID>` to execute specific PR group only

**Insert "Detect Execution Context"**:
- Check if running in worktree (auto-detect from `git worktree list`)
- Infer PR group from worktree path (e.g., `../worktrees/pr-001-auth` → `PR-001`)

**Modify "Load Task Registry"**:
- Filter tasks by PR group if specified or detected
- Log filtered task count

**Update agent invocation**:
- Pass `worktree_path` and `pr_group` to developer agents
- Set working directory to worktree

#### C. New Command: `/htec-sdd-worktree-setup`

**File**: `.claude/commands/htec-sdd-worktree-setup.md` (NEW)

**Purpose**: Execute generated worktree setup script

**Procedure**:
1. Validate script exists (`scripts/setup-worktrees.sh`)
2. Check git status (no uncommitted changes)
3. Execute setup script with base branch parameter
4. Verify worktrees created (`git worktree list`)
5. Report status with next steps

**Usage**:
```bash
/htec-sdd-worktree-setup InventorySystem
/htec-sdd-worktree-setup InventorySystem --base develop
```

### Phase 4: Worktree Coordination
**Duration**: 3-4 hours

#### A. Implementation Developer Updates

**File**: `.claude/agents/implementation-developer.md`

**Add "Worktree-Aware File Locking" section**:
- Lock scope determination (worktree vs global)
- Lock acquisition algorithm with worktree context
- Lock entry format with `worktree_path` and `lock_scope` fields

**Update invocation example**:
- Include `worktree_path` and `pr_group` in prompt
- Set `WORKING_DIR` to worktree location

#### B. Quality Agent Updates

**Files**: All 6 quality agents
- `quality-bug-hunter.md`
- `quality-security-auditor.md`
- `quality-code-quality.md`
- `quality-test-coverage.md`
- `quality-contracts-reviewer.md`
- `quality-accessibility-auditor.md`

**Add "PR-Scoped Review Mode" section**:
- Review only files within PR group scope
- Read PR metadata to get file list
- Invocation example with PR context

#### C. State Schema Updates

**`_state/agent_sessions.json`** - Add fields:
- `pr_group`: PR group ID
- `worktree_path`: Worktree location
- `branch`: Branch name
- `lock_scope`: "worktree" or "global"

**`_state/agent_lock.json`** - Add fields:
- `lock_scope`: "worktree" or "global"
- `worktree_path`: Worktree location (if scoped)
- `pr_group`: PR group ID
- `lock_key`: Unique key (worktree-scoped or global)

### Phase 5: Documentation Updates
**Duration**: 1-2 hours

#### Files to Update:

1. **`.claude/architecture/Agent_Spawning_Architecture.md`**
   - Remove hfe-ux/product-researcher from agent categories
   - Add "Worktree Coordination" section with lock scope rules

2. **`CLAUDE.md`** (root level)
   - Update `/htec-sdd-tasks` description to mention "interactive"
   - Add `/htec-sdd-worktree-setup` command
   - Add "Worktree Workflow" subsection with example

3. **`.claude/commands/HTEC_SDD_COMMAND_REFERENCE.md`**
   - Add `/htec-sdd-worktree-setup` to command list
   - Add "Worktree Workflow Example" section

4. **`.claude/architecture/workflows/Implementation Phase/Implementation_Phase_WoW.md`**
   - Update "Agent Architecture" section (remove research agents)
   - Add "Git Worktree Workflow" section
   - Update "Command Reference" with new command
   - Add "PR Grouping Strategy" section

---

## Critical Files to Modify

### High Priority (Core Changes)
1. `.claude/agents/planning-tech-lead.md` - Interactive strategy selection
2. `.claude/commands/htec-sdd-tasks.md` - Integrate user interaction, generate scripts
3. `.claude/agents/implementation-developer.md` - Worktree-aware locking
4. `.claude/commands/htec-sdd-worktree-setup.md` - NEW command

### Medium Priority (Supporting Changes)
5. `.claude/commands/htec-sdd-implement.md` - PR group filtering, worktree detection
6. `.claude/agents/quality-*.md` (6 files) - PR-scoped review mode
7. `.claude/agents/archived/README.md` - NEW archive explanation
8. `.claude/commands/agent-spawn.md` - Remove research agents from table

### Low Priority (Documentation)
9. `.claude/architecture/Agent_Spawning_Architecture.md` - Update agent taxonomy
10. `.claude/architecture/workflows/Implementation Phase/Implementation_Phase_WoW.md` - Update workflows
11. `CLAUDE.md` - Update command reference
12. `.claude/commands/HTEC_SDD_COMMAND_REFERENCE.md` - Update command list

---

## Verification Steps

### After Implementation:

1. **Test Agent Removal**:
   ```bash
   ls .claude/agents/archived/
   # Should see: planning-hfe-ux-researcher.md, planning-product-researcher.md, README.md
   ```

2. **Test Interactive Strategy Selection**:
   ```bash
   /htec-sdd-tasks TestSystem
   # Should present 4 questions and wait for user input
   ```

3. **Verify Worktree Setup**:
   ```bash
   cat Implementation_TestSystem/scripts/setup-worktrees.sh
   # Should contain git worktree add commands

   /htec-sdd-worktree-setup TestSystem
   git worktree list
   # Should show multiple worktrees
   ```

4. **Test PR-Scoped Execution**:
   ```bash
   cd ../worktrees/pr-001-auth
   /htec-sdd-implement --pr-group PR-001
   # Should execute only tasks in PR-001
   ```

5. **Verify File Locking**:
   ```bash
   # Spawn 2 developers in different worktrees modifying "same" file
   # Should NOT conflict (worktree-scoped locks)

   # Spawn 2 developers updating task_registry.json
   # Should conflict (global-scoped lock)
   ```

6. **Test PR Metadata**:
   ```bash
   cat Implementation_TestSystem/pr-metadata/PR-001.md
   # Should contain traceability matrix, test summary, file list
   ```

---

## Estimated Timeline

- **Phase 1** (Agent Removal): 30 minutes
- **Phase 2** (Tech-Lead): 2-3 hours
- **Phase 3** (Commands): 2-3 hours
- **Phase 4** (Worktree Coordination): 3-4 hours
- **Phase 5** (Documentation): 1-2 hours
- **Testing & Verification**: 2 hours

**Total**: 11-15 hours (1.5-2 days)

---

## Risk Mitigation

1. **User Interaction Blocks Automation**
   - Solution: Add `--auto` flag for non-interactive mode with sensible defaults

2. **File Locking Complexity**
   - Solution: Comprehensive logging, lock inspection command, clear documentation

3. **Worktree Cleanup**
   - Solution: Track worktrees in `_state/active_worktrees.json`, cleanup command

4. **Breaking Changes**
   - **Note**: This is a breaking change. Existing implementation sessions must restart from `/htec-sdd-init`
   - New schema required in task_registry.json
   - No backward compatibility with old format

---

## Success Criteria

- ✅ Research agents moved to archive (not deleted)
- ✅ Tech-lead presents 4 strategy questions before task decomposition
- ✅ Worktree setup script generates correctly
- ✅ PR metadata files include full traceability
- ✅ Developers can work in parallel worktrees without file conflicts
- ✅ Quality loop blocks on CRITICAL findings
- ✅ New schema correctly implemented in task_registry.json
- ✅ Documentation updated across all affected files

---

## Next Steps After Approval

1. Execute Phase 1 (Agent Removal) - Quick win
2. Execute Phase 2 (Tech-Lead) - Core enhancement
3. Execute Phase 3 (Commands) - Integration
4. Execute Phase 4 (Worktree Coordination) - Parallelization
5. Execute Phase 5 (Documentation) - Finalization
6. Run verification tests
7. Update CHANGELOG.md with new features
