#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import glob
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Configuration - Update this path to match your output directory
OUTPUT_DIR = "/home/amittal/Project/new_command"

def get_builds():
    """Get list of available builds"""
    builds = []
    if os.path.exists(OUTPUT_DIR):
        for item in os.listdir(OUTPUT_DIR):
            item_path = os.path.join(OUTPUT_DIR, item)
            if os.path.isdir(item_path) and item not in ['owner', 'rnd']:
                builds.append(item)
    return sorted(builds, reverse=True)

def get_failure_stats(build_dir):
    """Get failure statistics for a build"""
    stats = {}
    
    # Read status.txt if it exists
    status_file = os.path.join(build_dir, 'status.txt')
    if os.path.exists(status_file):
        try:
            df = pd.read_csv(status_file)
            for _, row in df.iterrows():
                stats[row['Category']] = row['Count']
        except Exception as e:
            print(f"Error reading status file: {e}")
            # Fallback to manual parsing
            with open(status_file, 'r') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        category = parts[0]
                        count = parts[1]
                        stats[category] = count
    
    return stats

def get_owner_files(build_dir):
    """Get list of owner HTML files"""
    owner_dir = os.path.join(build_dir, 'owner')
    files = []
    if os.path.exists(owner_dir):
        for file in os.listdir(owner_dir):
            if file.endswith('.html'):
                files.append(file)
    return sorted(files)

def get_main_files(build_dir):
    """Get list of main HTML files"""
    main_files = ['status_failure.html', 'status.html', 'AlreadyCCR.html']
    available_files = []
    
    for file in main_files:
        file_path = os.path.join(build_dir, file)
        if os.path.exists(file_path):
            available_files.append(file)
    
    return available_files

def get_csv_files(build_dir):
    """Get list of CSV files"""
    csv_files = []
    for file in os.listdir(build_dir):
        if file.endswith('.csv'):
            csv_files.append(file)
    return sorted(csv_files)

@app.route('/')
def index():
    """Main dashboard page"""
    builds = get_builds()
    
    if not builds:
        return render_template('no_builds.html')
    
    # Get selected build from query parameter
    selected_build = request.args.get('build', builds[0])
    if selected_build not in builds:
        selected_build = builds[0]
    
    build_dir = os.path.join(OUTPUT_DIR, selected_build)
    stats = get_failure_stats(build_dir)
    owner_files = get_owner_files(build_dir)
    main_files = get_main_files(build_dir)
    csv_files = get_csv_files(build_dir)
    
    return render_template('dashboard.html',
                         builds=builds,
                         selected_build=selected_build,
                         stats=stats,
                         owner_files=owner_files,
                         main_files=main_files,
                         csv_files=csv_files)

@app.route('/files/<build>/<path:filename>')
def serve_file(build, filename):
    """Serve HTML files from build directories"""
    file_path = os.path.join(OUTPUT_DIR, build, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(os.path.dirname(file_path), 
                                 os.path.basename(file_path))
    else:
        return "File not found", 404

@app.route('/files/<build>/owner/<path:filename>')
def serve_owner_file(build, filename):
    """Serve owner HTML files"""
    file_path = os.path.join(OUTPUT_DIR, build, 'owner', filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(os.path.dirname(file_path), 
                                 os.path.basename(file_path))
    else:
        return "File not found", 404

@app.route('/api/builds')
def api_builds():
    """API endpoint to get available builds"""
    builds = get_builds()
    return jsonify(builds)

@app.route('/api/stats/<build>')
def api_stats(build):
    """API endpoint to get build statistics"""
    build_dir = os.path.join(OUTPUT_DIR, build)
    stats = get_failure_stats(build_dir)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)