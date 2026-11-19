import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Amazon Bestseller Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #FFFFFF;
}

.subtitle {
    color: #A0AAB8;
    font-size: 15px;
}

.metric-card {
    background: linear-gradient(135deg, #1E293B, #263449);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #34445C;
}

.metric-label {
    color: #A0AAB8;
    font-size: 14px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: bold;
}

section[data-testid="stSidebar"] {
    background-color: #151B27;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "dataset/cleaned_bestsellers_2026.csv"
    )

    return df


df = load_data()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📚 BOOK INSIGHTS")

st.sidebar.caption("Amazon Bestseller Analytics")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Bestseller Analysis",
        "Author Analysis",
        "Price & Rating Analysis",
        "Raw Dataset"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("FILTERS")

authors = ["All"] + sorted(
    df["author"].dropna().unique().tolist()
)

selected_author = st.sidebar.selectbox(
    "Select Author",
    authors
)

formats = ["All"] + sorted(
    df["format"].dropna().unique().tolist()
)

selected_format = st.sidebar.selectbox(
    "Select Book Format",
    formats
)

filtered_df = df.copy()

if selected_author != "All":
    filtered_df = filtered_df[
        filtered_df["author"] == selected_author
    ]

if selected_format != "All":
    filtered_df = filtered_df[
        filtered_df["format"] == selected_format
    ]


if st.sidebar.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()


st.sidebar.caption(
    "Source: KDPTop API | Amazon US"
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">📚 Amazon Bestseller Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore bestseller rankings, authors, prices, ratings and reader engagement.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.caption(
    "Marketplace: Amazon US | Category: Literature & Fiction | "
    "Snapshot: November 2026"
)

st.divider()


# ==========================================
# HELPER FUNCTION FOR METRIC CARDS
# ==========================================

def metric_card(label, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# PAGE 1: OVERVIEW
# ==========================================

if page == "Overview":

    st.subheader("📊 Performance Overview")

    total_books = len(filtered_df)
    avg_rating = filtered_df["rating"].mean()
    avg_price = filtered_df["price"].mean()
    total_reviews = filtered_df["review_count"].sum()

    if total_reviews >= 1000:
        reviews_display = f"{total_reviews / 1000:.1f}K"
    else:
        reviews_display = f"{int(total_reviews):,}"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 TOTAL BOOKS", total_books)

    with col2:
        st.metric("⭐ AVERAGE RATING", f"{avg_rating:.2f}")

    with col3:
        st.metric("💰 AVERAGE PRICE", f"${avg_price:.2f}")

    with col4:
        st.metric("💬 TOTAL REVIEWS", reviews_display)

    st.write("")
    st.divider()

    # Bestseller table

    st.subheader("🏆 Top Bestselling Books")

    st.dataframe(
        filtered_df.sort_values("rank")[
            [
                "rank",
                "title",
                "author",
                "price",
                "rating",
                "review_count",
                "format"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Format and rating charts

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📖 Book Format Distribution")

        format_data = filtered_df["format"].value_counts()

        fig = px.pie(
            values=format_data.values,
            names=format_data.index,
            hole=0.55,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("⭐ Book Ratings")

        rating_data = filtered_df.sort_values(
            "rating",
            ascending=True
        )

        fig = px.bar(
            rating_data,
            x="rating",
            y="title",
            orientation="h",
            color="rating",
            template="plotly_dark",
            labels={
                "rating": "Rating",
                "title": "Book"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ==========================================
# PAGE 2: BESTSELLER ANALYSIS
# ==========================================

elif page == "Bestseller Analysis":

    st.subheader("🏆 Bestseller Ranking Analysis")

    rank_data = filtered_df.dropna(
        subset=["rank"]
    ).sort_values("rank", ascending=True)

    # TOP 5 BOOKS

    st.markdown("### 🌟 Top 5 Bestselling Books")

    top_5 = rank_data.head(5)

    st.dataframe(
        top_5[["rank", "title", "author", "price", "rating"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "rank": st.column_config.NumberColumn("Rank"),
            "title": st.column_config.TextColumn("Book Title"),
            "author": st.column_config.TextColumn("Author"),
            "price": st.column_config.NumberColumn(
                "Price ($)", format="$%.2f"
            ),
            "rating": st.column_config.NumberColumn(
                "Rating", format="⭐ %.2f"
            )
        }
    )

    st.divider()

    # BESTSELLER RANKING CHART

    st.markdown("### 📊 Bestseller Rankings")

    chart_data = rank_data.sort_values(
        "rank", ascending=False
    )

    fig = px.bar(
        chart_data,
        x="rank",
        y="title",
        orientation="h",
        color="rank",
        color_continuous_scale="RdYlGn_r",
        hover_name="title",
        hover_data=["author", "price", "rating"],
        title="Amazon Bestseller Rankings"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(
            autorange="reversed",
            title="Book Title"
        ),
        xaxis=dict(
            title="Bestseller Rank",
            dtick=1
        ),
        coloraxis_showscale=False,
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # RANKING MOVEMENT

    st.markdown("### 📈 Ranking Movement")

    movement_df = filtered_df.dropna(
        subset=["rank", "prev_rank"]
    ).copy()

    movement_df["Rank Change"] = (
        movement_df["prev_rank"] - movement_df["rank"]
    )

    movement_df["Movement"] = movement_df["Rank Change"].apply(
        lambda x: "Improved" if x > 0
        else ("Dropped" if x < 0 else "No Change")
    )

    if not movement_df.empty:

        # SUMMARY CARDS

        improved = (movement_df["Rank Change"] > 0).sum()
        dropped = (movement_df["Rank Change"] < 0).sum()
        unchanged = (movement_df["Rank Change"] == 0).sum()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🟢 Improved", improved)

        with col2:
            st.metric("🔴 Dropped", dropped)

        with col3:
            st.metric("⚪ No Change", unchanged)

        st.divider()

        # MOVEMENT CHART

        fig = px.bar(
            movement_df.sort_values("Rank Change"),
            x="Rank Change",
            y="title",
            orientation="h",
            color="Movement",
            color_discrete_map={
                "Improved": "#00CC96",
                "Dropped": "#EF553B",
                "No Change": "#636EFA"
            },
            hover_data=["author", "prev_rank", "rank"],
            title="Bestseller Ranking Changes"
        )

        fig.update_layout(
            template="plotly_dark",
            height=450,
            xaxis_title="Positions Improved (+) / Dropped (-)",
            yaxis_title="Book Title"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # COMPLETE RANKING TABLE

        st.markdown("### 📋 Complete Ranking Table")

        st.dataframe(
            movement_df[
                [
                    "rank", "title", "author",
                    "prev_rank", "Rank Change", "Movement"
                ]
            ].sort_values("rank"),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No previous ranking data available.")
    
# ==========================================
# PAGE 3: AUTHOR ANALYSIS
# ==========================================

elif page == "Author Analysis":

    st.subheader("✍️ Author Performance Analysis")

    # AUTHOR DATA

    author_data = (
        filtered_df.groupby("author", as_index=False)
        .agg(
            total_books=("title", "count"),
            average_rating=("rating", "mean"),
            total_reviews=("review_count", "sum")
        )
        .sort_values("total_books", ascending=False)
    )

    # SUMMARY METRICS

    total_authors = filtered_df["author"].nunique()
    avg_rating = filtered_df["rating"].mean()
    total_reviews = filtered_df["review_count"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("✍️ TOTAL AUTHORS", total_authors)

    with col2:
        st.metric(
            "⭐ AVERAGE RATING",
            f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A"
        )

    with col3:
        st.metric(
            "💬 TOTAL REVIEWS",
            f"{total_reviews:,.0f}"
        )

    st.divider()

    # BOOKS BY AUTHOR

    st.markdown("### 📚 Books by Author")

    fig = px.bar(
        author_data.sort_values("total_books"),
        x="total_books",
        y="author",
        orientation="h",
        color="total_books",
        color_continuous_scale="Viridis",
        text="total_books",
        title="Number of Bestselling Books by Author"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Number of Books",
        yaxis_title="Author",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # AUTHOR RATINGS

    st.markdown("### ⭐ Average Rating by Author")

    rating_data = author_data.dropna(
        subset=["average_rating"]
    ).sort_values("average_rating")

    fig = px.bar(
        rating_data,
        x="average_rating",
        y="author",
        orientation="h",
        color="average_rating",
        color_continuous_scale="Plasma",
        text="average_rating",
        title="Author Rating Comparison"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Average Rating",
        yaxis_title="Author",
        xaxis_range=[0, 5.5],
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # AUTHOR PERFORMANCE TABLE

    st.markdown("### 🏆 Author Performance Table")

    display_authors = author_data.rename(
        columns={
            "author": "Author",
            "total_books": "Total Books",
            "average_rating": "Average Rating",
            "total_reviews": "Total Reviews"
        }
    )

    st.dataframe(
        display_authors,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Average Rating": st.column_config.NumberColumn(
                format="%.2f"
            ),
            "Total Reviews": st.column_config.NumberColumn(
                format="%d"
            )
        }
    )

# ==========================================
# PAGE 4: PRICE AND RATING ANALYSIS
# ==========================================

elif page == "Price & Rating Analysis":

    st.subheader("💰 Price & Rating Analysis")

    # PRICE DATA

    price_data = filtered_df.dropna(
        subset=["price"]
    )

    # SUMMARY METRICS

    avg_price = price_data["price"].mean()
    min_price = price_data["price"].min()
    max_price = price_data["price"].max()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 AVERAGE PRICE",
            f"${avg_price:.2f}" if pd.notna(avg_price) else "N/A"
        )

    with col2:
        st.metric(
            "📉 LOWEST PRICE",
            f"${min_price:.2f}" if pd.notna(min_price) else "N/A"
        )

    with col3:
        st.metric(
            "📈 HIGHEST PRICE",
            f"${max_price:.2f}" if pd.notna(max_price) else "N/A"
        )

    st.divider()

    # PRICE DISTRIBUTION

    st.markdown("### 💵 Book Price Distribution")

    if not price_data.empty:

        fig = px.histogram(
            price_data,
            x="price",
            nbins=8,
            color_discrete_sequence=["#00CC96"],
            title="Distribution of Book Prices",
            labels={
                "price": "Book Price (USD)",
                "count": "Number of Books"
            }
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Book Price ($)",
            yaxis_title="Number of Books",
            bargap=0.15
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # BOOK RATINGS

    st.markdown("### ⭐ Book Rating Comparison")

    rating_data = filtered_df.dropna(
        subset=["rating"]
    ).sort_values("rating")

    if not rating_data.empty:

        fig = px.bar(
            rating_data,
            x="rating",
            y="title",
            orientation="h",
            color="rating",
            color_continuous_scale="Viridis",
            text="rating",
            hover_data=["author", "review_count"],
            title="Ratings of Bestselling Books"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Rating",
            yaxis_title="Book Title",
            xaxis_range=[0, 5.5],
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # REVIEWS VS RATINGS

    st.markdown("### 💬 Reviews vs Ratings")

    scatter_data = filtered_df.dropna(
        subset=["review_count", "rating"]
    )

    if not scatter_data.empty:

        fig = px.scatter(
            scatter_data,
            x="review_count",
            y="rating",
            color="format",
            size="price",
            hover_name="title",
            hover_data=["author", "price"],
            title="Relationship Between Reviews and Ratings"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Number of Reviews",
            yaxis_title="Book Rating"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # DESCRIPTIVE STATISTICS

    st.markdown("### 📊 Descriptive Statistics")

    stats_columns = [
        "price",
        "rating",
        "review_count",
        "rank"
    ]

    st.dataframe(
        filtered_df[stats_columns].describe(),
        use_container_width=True
    )


# ==========================================
# PAGE 5: RAW DATASET
# ==========================================

elif page == "Raw Dataset":

    st.subheader("📁 Complete Dataset")

    st.write(
        "Explore and download the collected Amazon bestseller records."
    )

    # DATASET OVERVIEW

    st.markdown("### 📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 TOTAL RECORDS", len(filtered_df))

    with col2:
        st.metric("📋 TOTAL COLUMNS", len(filtered_df.columns))

    with col3:
        st.metric(
            "🔁 DUPLICATE RECORDS",
            filtered_df.duplicated(subset=["asin"]).sum()
        )

    st.divider()

    # SEARCH DATASET

    st.markdown("### 🔍 Search Books")

    search_text = st.text_input(
        "Search by book title or author"
    )

    display_df = filtered_df.copy()

    if search_text:
        display_df = display_df[
            display_df["title"].str.contains(
                search_text, case=False, na=False
            )
            |
            display_df["author"].str.contains(
                search_text, case=False, na=False
            )
        ]

    # DATA TABLE

    st.markdown("### 📋 Dataset Records")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Displaying {len(display_df)} of {len(filtered_df)} records."
    )

    st.divider()

    # MISSING VALUE ANALYSIS

    st.markdown("### ⚠️ Missing Value Analysis")

    missing_data = filtered_df.isnull().sum().reset_index()

    missing_data.columns = ["Column", "Missing Values"]

    missing_data["Missing Percentage"] = (
        missing_data["Missing Values"]
        / max(len(filtered_df), 1) * 100
    ).round(2)

    missing_data = missing_data[
        missing_data["Missing Values"] > 0
    ]

    if not missing_data.empty:

        st.dataframe(
            missing_data,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No missing values found.")

    st.divider()

    # DOWNLOAD DATASET

    st.markdown("### 📥 Download Dataset")

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Complete Dataset (CSV)",
        data=csv,
        file_name="amazon_bestsellers_2026.csv",
        mime="text/csv"
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Amazon Bestseller Analytics Dashboard | "
    "Developed using Python, Pandas, Plotly and Streamlit"
)

st.caption(
    "Data source: KDPTop API | "
    "Rankings represent the captured snapshot, not continuous live data."
)
