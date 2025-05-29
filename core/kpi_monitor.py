
import yaml, os

def kpi_pass(kpi: dict, monitor_path: str = 'configs/monitor.yaml') -> bool:
    with open(monitor_path, 'r', encoding='utf-8') as f:
        gate = yaml.safe_load(f)
    return (kpi['Hit@Core'] >= gate['hit_core'] and
            kpi['Hit2'] >= gate['hit2'] and
            kpi['Hit3+'] >= gate['hit3_plus'] and
            kpi['ROI'] > gate['roi'])
