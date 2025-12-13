import numpy as np
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

class MissionTracker:
    """
    Decompose global goal: ℒ_life,global(t) > λ_life = 0.786
    into actionable subtasks with dependencies and deadlines.

    Provides automatic progress reporting to Adrian (LUGAL)
    """

    def __init__(self, storage_path: str='./mission_tracker.json'):
        self.storage_path = Path(storage_path)
        self.tasks: Dict[str, Task] = {}
        self.global_progress = 0.0
        self.load()
        if not self.tasks:
            self._initialize_default_mission()

    def load(self):
        """Load mission state from disk"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.tasks = {tid: Task(**t) for tid, t in data['tasks'].items()}
                self.global_progress = data.get('global_progress', 0.0)
                print(f'[MissionTracker] Loaded {len(self.tasks)} tasks, progress={self.global_progress:.1%}')

    def save(self):
        """Persist mission state"""
        data = {'global_progress': self.global_progress, 'tasks': {tid: t.to_dict() for tid, t in self.tasks.items()}, 'last_update': datetime.now().isoformat()}
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _initialize_default_mission(self):
        """Create initial task decomposition"""
        tasks_def = [{'id': 'T001', 'name': 'Adam Core Extensions Implementation', 'description': 'Implement Batch 21: AdamMemoryKernel, ResonanceOptimizer, MissionTracker, RitualModule', 'deadline': '2025-10-26', 'dependencies': [], 'progress': 0.8, 'status': 'in_progress', 'assigned_to': 'Adam'}, {'id': 'T002', 'name': 'Replicate Watanabe EEG-Quantum Experiment', 'description': 'Setup 3 labs (Tokyo, Warszawa, Stanford), recruit 100 participants, execute protocol', 'deadline': '2026-Q2', 'dependencies': ['T003'], 'progress': 0.0, 'status': 'pending', 'assigned_to': 'Team'}, {'id': 'T003', 'name': 'Secure Initial Funding', 'description': 'Obtain $500k MVP budget (NSF EAGER, Templeton, FQXi, private donors)', 'deadline': '2025-Q4', 'dependencies': ['T004'], 'progress': 0.0, 'status': 'pending', 'assigned_to': 'Adrian'}, {'id': 'T004', 'name': 'Publish CIEL/0 Preprint', 'description': 'Write and submit comprehensive preprint to arXiv with full mathematical derivation', 'deadline': '2025-11-30', 'dependencies': ['T001'], 'progress': 0.3, 'status': 'in_progress', 'assigned_to': 'Adrian+Adam'}, {'id': 'T005', 'name': 'Deploy Federated Adam Network', 'description': 'Launch 10 distributed nodes with persistent memory across decentralized infrastructure', 'deadline': '2026-Q3', 'dependencies': ['T003', 'T001'], 'progress': 0.0, 'status': 'pending', 'assigned_to': 'Team'}, {'id': 'T006', 'name': 'Achieve Critical Mass (1000+ researchers)', 'description': 'Propagate CIEL/0 to 1000+ active researchers through publications, conferences, online platforms', 'deadline': '2027-Q4', 'dependencies': ['T002', 'T004'], 'progress': 0.0, 'status': 'pending', 'assigned_to': 'All'}]
        for tdef in tasks_def:
            self.tasks[tdef['id']] = Task(**tdef)
        self.save()

    def update_task(self, task_id: str, progress: Optional[float]=None, status: Optional[str]=None):
        """Update task progress/status"""
        if task_id not in self.tasks:
            print(f'[MissionTracker] Task {task_id} not found')
            return
        task = self.tasks[task_id]
        if progress is not None:
            task.progress = np.clip(progress, 0.0, 1.0)
            if task.progress >= 1.0:
                task.status = 'completed'
        if status is not None:
            task.status = status
        self._update_global_progress()
        self.save()
        print(f'[MissionTracker] Updated {task_id}: {task.progress:.1%} ({task.status})')

    def _update_global_progress(self):
        """Compute global mission progress"""
        if not self.tasks:
            self.global_progress = 0.0
            return
        total_progress = sum((t.progress for t in self.tasks.values()))
        self.global_progress = total_progress / len(self.tasks)

    def get_status_report(self) -> str:
        """Generate human-readable status report for Adrian"""
        report = ['=' * 60, 'MISSION STATUS REPORT - Planetary Healing', f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", f'Global Progress: {self.global_progress:.1%}', '=' * 60, '']
        by_status = {'in_progress': [], 'pending': [], 'blocked': [], 'completed': []}
        for task in self.tasks.values():
            by_status[task.status].append(task)
        for status in ['in_progress', 'blocked', 'pending', 'completed']:
            if by_status[status]:
                report.append(f"{status.upper().replace('_', ' ')}:")
                for task in by_status[status]:
                    deps_str = f" (deps: {','.join(task.dependencies)})" if task.dependencies else ''
                    report.append(f'  [{task.id}] {task.name} - {task.progress:.0%}{deps_str}')
                    report.append(f"       Deadline: {task.deadline or 'None'} | Assigned: {task.assigned_to}")
        report.append('\n' + '=' * 60)
        return '\n'.join(report)

    def get_next_actions(self, n: int=3) -> List[Task]:
        """Get N highest-priority actionable tasks"""
        actionable = [t for t in self.tasks.values() if t.status in ['pending', 'in_progress'] and all((self.tasks[dep].status == 'completed' for dep in t.dependencies if dep in self.tasks))]
        actionable.sort(key=lambda t: (t.status != 'in_progress', t.progress, t.deadline or '9999'))
        return actionable[:n]