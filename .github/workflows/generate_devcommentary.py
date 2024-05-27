
import os
import pandas as pd

# CSV 파일들을 읽어와서 데이터프레임으로 변환
csv_files = [f for f in os.listdir('_DevCommentary') if f.endswith('.csv')]
df_list = []
for file in csv_files:
    df = pd.read_csv(f'_DevCommentary/{file}', names=['week', 'platform', 'problem', 'url', 'name'])
    df_list.append(df)

# 데이터프레임 합치기
df = pd.concat(df_list, ignore_index=True)

# 주차별로 그룹화
weeks = df['week'].unique()

# README 파일 생성
with open('_DevCommentary/README.md', 'w') as f:
    for week in weeks:
        f.write(f'## {week} 해설글\n')
        
        # 플랫폼별로 그룹화
        platforms = df[df['week'] == week]['platform'].unique()
        
        for platform in platforms:
            f.write(f'<details>\n<summary>{platform}</summary>\n\n')
            
            # 문제별 해설글을 테이블로 정리
            f.write('| 문제 | 해설글 |\n')
            f.write('| --- | --- |\n')
            
            # 문제별로 그룹화
            problems = df[(df['week'] == week) & (df['platform'] == platform)]['problem'].unique()
            
            for problem in problems:
                # 해당 문제에 대한 해설글 작성자와 URL
                problem_df = df[(df['week'] == week) & (df['platform'] == platform) & (df['problem'] == problem)]
                
                f.write(f'| {problem} | ')
                
                for i, (_, row) in enumerate(problem_df.iterrows()):
                    f.write(f"[{row['name']}의 해설글]({row['url']})")
                    
                    if i < len(problem_df) - 1:
                        f.write('<br>')
                
                f.write(' |\n')
            
            f.write('\n</details>\n\n')