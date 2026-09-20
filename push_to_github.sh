#!/bin/bash
# Push Script for GeoHealth Sentinel (Nellore City & Kovur Mandal)
# Configured for @virahitvin8

echo "=========================================================="
echo "🚀 Pushing Health GIS Project to GitHub for @virahitvin8..."
echo "=========================================================="

cd /workspace/interactive-project || exit 1

# Ensure on main branch
git branch -M main

# Push to authenticated origin
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Project pushed to: https://github.com/virahitvin8/nellore-health-gis"
    echo "👉 Now enable GitHub Pages in Settings -> Pages -> Deploy from main -> Save"
    echo "🌐 Live link will be: https://virahitvin8.github.io/nellore-health-gis/"
else
    echo ""
    echo "⚠️  Push failed because the repository 'nellore-health-gis' does not exist yet on GitHub."
    echo "👉 Please create the empty repository first by clicking this pre-filled link:"
    echo "   https://github.com/new?name=nellore-health-gis"
    echo "Then re-run: ./push_to_github.sh"
fi
