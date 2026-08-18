import os,sys
from pathlib import Path

def project_root(marker='.git'):
    for parent in Path(__file__).resolve().parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"No {marker} found above {__file__}")


PROJECT_DIR = project_root()
sys.path.insert(0, str(PROJECT_DIR)) 
RAW_DIR     = PROJECT_DIR / "raw_data" / "daily_rosters"
ARCHIVE_DIR = RAW_DIR / "archive"

files=sorted(ARCHIVE_DIR.glob("*.json"))
total_files=(len(files))


def find_same_day(days):
    entry_list=[]
    n=0
    days.sort()
    for i in range(len(days)):
        if i == len(days)-1 or days[i] != days[i+1]:
            entry_list.append((days[i],n+1))
            n=0
        else:
            n += 1
    return(entry_list)   
        


days=[]
for file in files:
    toks=file.parts[8].split('_')
    datetim=(toks[3].split('.'))
    day=(datetim[0][0:8])
    days.append(day)
day_set = set(days)
unique_days=len(day_set)

print(f"Total Files:  {total_files}")
print(f"Unique Days:  {unique_days}")
   
day_list=list(day_set)
day_list.sort()
for day in day_list:
    print(day)
    
entries = find_same_day(days)

for day, entries in entries:
    print(f"Day: {day}  Number of entries: {entries}")
 
    