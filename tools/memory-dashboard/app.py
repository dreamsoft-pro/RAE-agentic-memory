"""
RAE Memory Dashboard - Main Application

Enterprise-grade Streamlit dashboard for RAE Memory Engine.
Provides visualization and management of agent memories.

Features:
- Real-time memory statistics
- Timeline visualization
- Knowledge graph explorer
- Memory editor
- Query inspector
"""

import os

import streamlit as st
from utils.api_client import RAEClient, get_cached_stats
from utils.visualizations import (
    apply_custom_css,
    create_layer_distribution_chart,
    create_tags_wordcloud_chart,
)

# Page configuration
st.set_page_config(
    page_title="RAE Memory Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://docs.rae-memory.dev",
        "Report a bug": "https://github.com/your-org/rae-agentic-memory/issues",
        "About": "RAE Memory Dashboard v1.0.0 - Enterprise Memory Management",
    },
)

# Apply custom styling
apply_custom_css()

# Title and description
st.title("🧠 RAE Memory Dashboard")
st.markdown(
    """
Enterprise-grade dashboard for visualizing and managing your AI agent's memory.

**Features:**
- 📊 Real-time statistics and analytics
- 📅 Timeline visualization
- 🕸️ Knowledge graph explorer
- ✏️ Memory editor
- 🔍 Query inspector
"""
)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Initialize session state for config if not exists
    if "config" not in st.session_state:
        st.session_state.config = {
            "api_url": os.getenv("RAE_API_URL", "http://localhost:8000"),
            "api_key": os.getenv("RAE_API_KEY", "default-key"),
            "tenant_id": os.getenv("RAE_TENANT_ID", "default-tenant"),
            "project_id": os.getenv("RAE_PROJECT_ID", "default-project"),
        }

    # Connection settings
    with st.expander("API Connection", expanded=True):
        api_url = st.text_input(
            "API URL",
            value=st.session_state.config["api_url"],
            help="URL of the RAE Memory API",
        )

        api_key = st.text_input(
            "API Key",
            value=st.session_state.config["api_key"],
            type="password",
            help="API authentication key",
        )

        tenant_id = st.text_input(
            "Tenant ID",
            value=st.session_state.config["tenant_id"],
            help="Tenant identifier for multi-tenancy",
        )

        project_id = st.text_input(
            "Project ID",
            value=st.session_state.config["project_id"],
            help="Project identifier",
        )

    # Connection button
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔌 Connect", type="primary", use_container_width=True):
            try:
                # Update config in session state
                st.session_state.config.update({
                    "api_url": api_url,
                    "api_key": api_key,
                    "tenant_id": tenant_id,
                    "project_id": project_id,
                })
                
                client = RAEClient(
                    api_url=api_url,
                    api_key=api_key,
                    tenant_id=tenant_id,
                    project_id=project_id,
                )

                # Test connection
                if client.test_connection():
                    st.session_state.client = client
                    st.session_state.connected = True
                    st.success("✓ Connected!")
                    st.rerun()
                else:
                    st.error("❌ Connection failed")
                    st.session_state.connected = False

            except Exception as e:
                st.error(f"❌ Connection error: {e}")
                st.session_state.connected = False

    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Connection status
    if st.session_state.get("connected", False):
        st.success("🟢 Connected")
    else:
        st.warning("🔴 Not connected")

    # Help section
    with st.expander("ℹ️ Help"):
        st.markdown(
            """
        **Quick Start:**
        1. Configure connection settings
        2. Click "Connect"
        3. Navigate to pages in sidebar

        **Pages:**
        - **Timeline**: View memory timeline
        - **Knowledge Graph**: Explore relationships
        - **Memory Editor**: Edit memories
        - **Query Inspector**: Test queries

        **Troubleshooting:**
        - Ensure RAE API is running
        - Check API URL and credentials
        - Click "Refresh" to reload data
        """
        )

# Main content area
if "connected" in st.session_state and st.session_state.connected:
    client = st.session_state.client

    st.divider()

    # Overview section
    st.header("📊 Overview")

    # Fetch statistics
    try:
        stats = get_cached_stats(client)

        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Total Memories",
                stats.get("total", 0),
                help="Total number of memories stored",
            )

        with col2:
            st.metric(
                "Episodic", stats.get("episodic", 0), help="Recent event memories"
            )

        with col3:
            st.metric(
                "Working", stats.get("working", 0), help="Current context memories"
            )

        with col4:
            st.metric(
                "Semantic",
                stats.get("semantic", 0),
                help="Concept and guideline memories",
            )

        with col5:
            st.metric(
                "Long-term", stats.get("ltm", 0), help="Consolidated long-term memories"
            )

    except Exception as e:
        st.error(f"Error fetching statistics: {e}")

    st.divider()

    # Quick visualizations
    st.header("📈 Quick Analytics")

    tab1, tab2, tab3 = st.tabs(["Recent Activity", "Layer Distribution", "Top Tags"])

    with tab1:
        try:
            recent_memories = client.get_memories(limit=50)

            if recent_memories:
                st.subheader("Recent Memory Activity")
                st.caption(f"Showing last {len(recent_memories)} memories")

                # Display recent memories
                for memory in recent_memories[:10]:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])

                        with col1:
                            content = memory.get("content", "")
                            if len(content) > 100:
                                content = content[:100] + "..."
                            st.text(content)

                        with col2:
                            st.caption(memory.get("layer", "N/A"))

                        with col3:
                            if "timestamp" in memory:
                                st.caption(memory["timestamp"][:10])

                        st.divider()
            else:
                st.info("No recent memories found")

        except Exception as e:
            st.error(f"Error fetching recent memories: {e}")

    with tab2:
        try:
            memories = client.get_memories(limit=100)

            if memories:
                fig = create_layer_distribution_chart(memories)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for visualization")

        except Exception as e:
            st.error(f"Error creating chart: {e}")

    with tab3:
        try:
            memories = client.get_memories(limit=100)

            if memories:
                fig = create_tags_wordcloud_chart(memories)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No tags found")

        except Exception as e:
            st.error(f"Error creating tag chart: {e}")

    st.divider()

    # Project reflection
    st.header("🔮 Project Reflection")

    with st.expander("View Current Project Reflection"):
        try:
            with st.spinner("Generating reflection..."):
                reflection = client.get_reflection()
                st.markdown(reflection)
        except Exception as e:
            st.error(f"Error fetching reflection: {e}")

    # Footer
    st.divider()
    st.caption("RAE Memory Dashboard v1.0.0 | Enterprise Memory Management")

else:
    # Not connected - show welcome message
    st.info(
        "👈 Please configure connection settings in the sidebar and click 'Connect'"
    )

    st.divider()

    # Welcome content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Getting Started")
        st.markdown(
            """
        1. **Start RAE API**
           ```bash
           docker-compose up -d
           ```

        2. **Configure Connection**
           - Enter API URL (default: http://localhost:8000)
           - Set API key and tenant ID
           - Click "Connect"

        3. **Explore Dashboard**
           - View timeline
           - Explore knowledge graph
           - Edit memories
           - Test queries
        """
        )

    with col2:
        st.subheader("📚 Features")
        st.markdown(
            """
        **Timeline Visualization**
        - View memory history
        - Filter by layer and date
        - Interactive charts

        **Knowledge Graph**
        - Explore relationships
        - Visual network graph
        - Node and edge details

        **Memory Editor**
        - Search and edit memories
        - Update content and tags
        - Delete memories

        **Query Inspector**
        - Test search queries
        - View ranked results
        - Inspect scoring
        """
        )

    st.divider()

    # Example connection
    st.subheader("💡 Example Configuration")

    st.code(
        """
API URL: http://localhost:8000
API Key: your-api-key
Tenant ID: default-tenant
Project ID: my-project
    """,
        language="text",
    )

    st.caption("Ensure RAE Memory API is running and accessible at the specified URL.")
