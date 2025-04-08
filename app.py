from shiny import App, ui
import pandas as pd
import plotly.express as px
import io

# Load data from CSV file
df = pd.read_csv("quakes-cleaned.csv")

# Prepare data for visualizations
df["local_area"] = df["place"].str.split(",").str[-1].str.strip()

def local_area_frequency():
    df2 = df["local_area"].value_counts().reset_index()
    df2.columns = ["local_area", "area_counts"]
    fig = px.bar(
        df2.head(10),
        x="local_area",
        y="area_counts",
        title="Distribution of Local Areas by frequency of earthquakes",
        labels={"local_area": "Local Area", "area_counts": "Count of earthquakes"},
        color_discrete_sequence=["black"],
    )
    return fig

def max_magnitude():
    largest_events_by_place = df.loc[df.groupby("local_area")["mag"].idxmax()]
    result = largest_events_by_place[["local_area", "mag"]].sort_values(by="mag", ascending=False)
    fig = px.bar(
        result.head(10),
        x="local_area",
        y="mag",
        title="Maximum value of earthquake at each location",
        labels={"local_area": "Local Area", "mag": "Magnitude of earthquake"},
        color_discrete_sequence=["black"],
    )
    return fig

def avg_mag_error_scatter():
    average_mag_error = df.groupby("magNst")["magError"].mean().reset_index()
    average_mag_error.columns = ["magNst", "avg_magError"]
    fig = px.scatter(
        average_mag_error,
        x="magNst",
        y="avg_magError",
        trendline="ols",
        title="Average magError by magNst",
        labels={"magNst": "Number of Stations", "avg_magError": "Average magError"},
    )
    return fig

def latitude_pie():
    df["latitude_group"] = df["latitude"].apply(lambda x: "North" if x >= 0 else "South")
    latitude_group_counts = df["latitude_group"].value_counts().reset_index()
    latitude_group_counts.columns = ["latitude_group", "frequency"]
    fig = px.pie(
        latitude_group_counts,
        names="latitude_group",
        values="frequency",
        title="Frequency of Earthquakes: Northern vs Southern Hemisphere",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    return fig

def longitude_pie():
    df["longitude_group"] = df["longitude"].apply(lambda x: "East" if x >= 0 else "West")
    longitude_group_counts = df["longitude_group"].value_counts().reset_index()
    longitude_group_counts.columns = ["longitude_group", "frequency"]
    fig = px.pie(
        longitude_group_counts,
        names="longitude_group",
        values="frequency",
        title="Frequency of Earthquakes: Eastern vs Western Hemisphere",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    return fig

def render_plotly_as_html(fig):
    """Convert Plotly figure to HTML string."""
    buffer = io.StringIO()
    fig.write_html(buffer, full_html=False)
    buffer.seek(0)
    return buffer.read()

app_ui = ui.page_fluid(
    ui.tags.h1("Programming for Data Scientists", class_="text-center"),
    ui.tags.h3("CA-3: Pandas – Plotting – Publishing", class_="text-center"),
    ui.tags.h5("By - Mitul Srivastava (C00313606)", class_="text-center"),
    ui.div(
        ui.HTML(render_plotly_as_html(local_area_frequency())),
        ui.HTML(render_plotly_as_html(max_magnitude())),
        ui.HTML(render_plotly_as_html(avg_mag_error_scatter())),
        ui.HTML(render_plotly_as_html(latitude_pie())),
        ui.HTML(render_plotly_as_html(longitude_pie()))
    )
)

def server(input, output, session):
    pass  # No input/output handling needed for static rendering

app = App(app_ui, server)
