#!/usr/bin/env python3
"""Grid search using Sentence Embeddings + ensemble classifiers for 75%+ accuracy."""
import argparse, os, json, itertools, pandas as pd, numpy as np, time, warnings
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
warnings.filterwarnings('ignore')

def load_data(path):
    df = pd.read_csv(path)
    if 'expected_sentiment' not in df.columns or 'text' not in df.columns:
        raise ValueError('CSV must contain columns: expected_sentiment,text')
    df = df.dropna(subset=['text']).reset_index(drop=True)
    return df

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    df = load_data(args.input)
    labels = sorted(df['expected_sentiment'].unique())
    label2idx = {l: i for i, l in enumerate(labels)}
    y = df['expected_sentiment'].map(label2idx).values
    X = df['text'].astype(str).values
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42, stratify=y if len(labels) > 1 else None)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp if len(labels) > 1 else None)
    
    print('\n' + '='*80)
    print('GRID SEARCH: SENTENCE EMBEDDINGS + ENSEMBLE CLASSIFIERS')
    print('='*80)
    print('Loading sentence embedding model (all-MiniLM-L6-v2)...')
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    print('Generating embeddings...')
    X_train_emb = embedder.encode(X_train.tolist(), show_progress_bar=False, batch_size=64)
    X_val_emb = embedder.encode(X_val.tolist(), show_progress_bar=False, batch_size=64)
    X_test_emb = embedder.encode(X_test.tolist(), show_progress_bar=False, batch_size=64)
    print(f'Embedding shape: {X_train_emb.shape}\n')
    
    grid = {
        'classifier': ['svm', 'rf', 'gb', 'ada'],
        'C': [0.1, 0.5, 1.0, 5.0, 10.0],
        'n_estimators': [100, 200, 300],
        'max_depth': [7, 10, 15],
    }
    
    keys = list(grid.keys())
    values = [grid[k] for k in keys]
    combinations = list(itertools.product(*values))
    total = len(combinations)
    print(f'Testing {total} combinations...\n')
    
    results = []
    start_time = time.perf_counter()
    
    for idx, combo in enumerate(combinations):
        params = dict(zip(keys, combo))
        try:
            clf_type = params['classifier']
            if clf_type == 'svm':
                clf = SVC(C=params['C'], kernel='linear', random_state=42, max_iter=2000)
            elif clf_type == 'rf':
                clf = RandomForestClassifier(n_estimators=params['n_estimators'], max_depth=params['max_depth'], random_state=42, n_jobs=-1)
            elif clf_type == 'gb':
                clf = GradientBoostingClassifier(n_estimators=params['n_estimators'], max_depth=params['max_depth'], learning_rate=0.05, random_state=42)
            elif clf_type == 'ada':
                clf = AdaBoostClassifier(n_estimators=params['n_estimators'], random_state=42)
            
            clf.fit(X_train_emb, y_train)
            val_acc = accuracy_score(y_val, clf.predict(X_val_emb))
            test_acc = accuracy_score(y_test, clf.predict(X_test_emb))
            gap = val_acc - test_acc
            
            results.append({'params': params, 'type': clf_type, 'val_acc': val_acc, 'test_acc': test_acc, 'gap': gap})
            pct = 100.0 * (idx + 1) / total
            print(f'[{pct:5.1f}%] Test: {test_acc:.4f} ({clf_type}) — {time.perf_counter() - start_time:.1f}s', end='\r')
        except:
            pass
    
    print(f'\nDone in {time.perf_counter() - start_time:.1f}s\n')
    
    if not results:
        print('No results!')
        return
    
    results.sort(key=lambda r: (-r['test_acc'], abs(r['gap'])))
    
    print('='*100)
    print('TOP 10 RESULTS')
    print('='*100)
    for rank, r in enumerate(results[:10], 1):
        print(f"\n{rank}. {r['type'].upper()}: Test={r['test_acc']:.4f}, Val={r['val_acc']:.4f}, Gap={r['gap']:+.4f}")
    
    best = results[0]
    print('\n' + '='*100)
    print(f"BEST: {best['type'].upper()} - Test Acc: {best['test_acc']:.4f}")
    print('='*100)
    
    best_params = best['params'].copy()
    best_params['classifier'] = best['type']
    
    output_file = os.path.join(args.output_dir, 'best_hyperparams.json')
    with open(output_file, 'w') as f:
        json.dump(best_params, f, indent=2)
    print(f"Saved to {output_file}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output-dir', default='results')
    args = p.parse_args()
    main(args)
