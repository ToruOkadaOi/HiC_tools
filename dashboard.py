#!/usr/bin/env python3
"""
Hi-C Tools Interactive Dashboard
A Streamlit-based interactive visualization for exploring Hi-C data analysis tools
"""

import streamlit as st
import re
from collections import defaultdict

# Page configuration
st.set_page_config(
    page_title="Hi-C Tools Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .tool-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
        transition: all 0.3s ease;
    }
    .tool-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .category-badge {
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        margin-right: 5px;
        display: inline-block;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
    }
    .stat-number {
        font-size: 36px;
        font-weight: bold;
    }
    .stat-label {
        font-size: 14px;
        opacity: 0.9;
    }
    h1 {
        color: #2E86AB;
    }
    h2 {
        color: #5C8AB8;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def parse_readme():
    """Parse README.md and extract tools information"""
    tools = []
    categories = defaultdict(list)
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by sections (headers starting with ##)
        sections = re.split(r'\n## ', content)
        current_category = "General"
        
        for section in sections:
            lines = section.split('\n')
            if not lines:
                continue
                
            # Get category name from first line
            category_match = re.match(r'^([^#\n]+)', lines[0])
            if category_match:
                current_category = category_match.group(1).strip()
            
            # Skip table of content and general sections
            if current_category in ["Table of content", "How to View This README"]:
                continue
            
            # Find all tools in this section (lines starting with -)
            for i, line in enumerate(lines):
                # Match tool entries
                tool_match = re.match(r'^-\s*(?:<a name="([^"]+)">)?\[([^\]]+)\]\(([^)]+)\)', line)
                if tool_match:
                    tool_id = tool_match.group(1) or ""
                    tool_name = tool_match.group(2)
                    tool_url = tool_match.group(3)
                    
                    # Get description (text after the link)
                    description = line[tool_match.end():].strip()
                    if description.startswith('- '):
                        description = description[2:].strip()
                    
                    # Clean up description
                    description = re.sub(r'<details>.*', '', description, flags=re.DOTALL)
                    description = description[:300] + "..." if len(description) > 300 else description
                    
                    tool_info = {
                        'name': tool_name,
                        'url': tool_url,
                        'category': current_category,
                        'description': description,
                        'id': tool_id
                    }
                    
                    tools.append(tool_info)
                    categories[current_category].append(tool_info)
        
        return tools, dict(categories)
    
    except Exception as e:
        st.error(f"Error parsing README: {e}")
        return [], {}

def display_tool_card(tool):
    """Display a tool as a card"""
    st.markdown(f"""
    <div class="tool-card">
        <h3>🔧 {tool['name']}</h3>
        <span class="category-badge">{tool['category']}</span>
        <p>{tool['description']}</p>
        <p><a href="{tool['url']}" target="_blank">🔗 Visit Project</a></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("# 🧬 Hi-C Tools Explorer Dashboard")
    st.markdown("### An interactive way to discover and explore Hi-C data analysis tools")
    
    # Load data
    tools, categories = parse_readme()
    
    if not tools:
        st.error("No tools found. Please check if README.md is available.")
        return
    
    # Sidebar filters
    st.sidebar.title("🔍 Filter & Search")
    
    # Search box
    search_query = st.sidebar.text_input("Search tools", "", placeholder="Type tool name or keyword...")
    
    # Category filter
    all_categories = ["All"] + sorted(list(categories.keys()))
    selected_category = st.sidebar.selectbox("Filter by Category", all_categories)
    
    # View mode
    view_mode = st.sidebar.radio("View Mode", ["Cards", "Table", "Kanban Board"])
    
    # Stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statistics")
    st.sidebar.metric("Total Tools", len(tools))
    st.sidebar.metric("Categories", len(categories))
    
    # Main content area
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(tools)}</div>
            <div class="stat-label">Total Tools</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(categories)}</div>
            <div class="stat-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        filtered_count = len(tools)
        if selected_category != "All":
            filtered_count = len(categories.get(selected_category, []))
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{filtered_count}</div>
            <div class="stat-label">Showing</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filter tools based on search and category
    filtered_tools = tools
    
    if search_query:
        filtered_tools = [
            t for t in filtered_tools 
            if search_query.lower() in t['name'].lower() 
            or search_query.lower() in t['description'].lower()
            or search_query.lower() in t['category'].lower()
        ]
    
    if selected_category != "All":
        filtered_tools = [t for t in filtered_tools if t['category'] == selected_category]
    
    # Display results
    if not filtered_tools:
        st.warning("No tools match your search criteria.")
        return
    
    st.markdown(f"## Showing {len(filtered_tools)} tool(s)")
    
    # Display based on view mode
    if view_mode == "Cards":
        # Card view
        for tool in filtered_tools:
            display_tool_card(tool)
    
    elif view_mode == "Table":
        # Table view
        import pandas as pd
        df = pd.DataFrame(filtered_tools)
        df = df[['name', 'category', 'description', 'url']]
        
        # Make URLs clickable
        st.dataframe(
            df,
            column_config={
                "url": st.column_config.LinkColumn("Link"),
                "name": "Tool Name",
                "category": "Category",
                "description": "Description"
            },
            hide_index=True,
            use_container_width=True
        )
    
    elif view_mode == "Kanban Board":
        # Kanban board view - group by category
        if selected_category == "All":
            # Show multiple columns for different categories
            kanban_categories = list(set(t['category'] for t in filtered_tools))[:6]  # Show first 6 categories
        else:
            kanban_categories = [selected_category]
        
        cols = st.columns(len(kanban_categories))
        
        for idx, category in enumerate(kanban_categories):
            with cols[idx]:
                st.markdown(f"### {category}")
                category_tools = [t for t in filtered_tools if t['category'] == category]
                for tool in category_tools[:10]:  # Show up to 10 tools per column
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #2196F3;">
                        <strong>{tool['name']}</strong><br/>
                        <small>{tool['description'][:100]}...</small><br/>
                        <a href="{tool['url']}" target="_blank">🔗</a>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>💡 <strong>Tip:</strong> Use the sidebar to filter tools by category or search for specific functionality</p>
        <p>📚 Full documentation available in <a href="README.md">README.md</a></p>
        <p>🌟 Want to contribute? Check out <a href="CONTRIBUTING.md">CONTRIBUTING.md</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
