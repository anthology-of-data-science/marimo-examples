import marimo

__generated_with = "0.18.0"
app = marimo.App(
    width="medium",
    layout_file="layouts/gpx_viewer_altair.grid.json",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    import geopandas as gpd
    import altair as alt
    import altair_tiles as til


    f = mo.ui.file(filetypes=[".gpx"], multiple=False)
    provider = mo.ui.dropdown(
        options={
            "Stamen Terrain": "Stadia.StamenTerrain",
            "Alidade Smooth": "Stadia.AlidadeSmooth",
            "Stamen Toner": "Stadia.StamenToner",
            "OSM CAT": "OpenStreetMap.CAT",
            "OSM HOT": "OpenStreetMap.HOT",
        },
        value="Stamen Terrain",  # initial value
        label="choose map provider",
    )
    mo.vstack([mo.hstack([mo.md("Please upload a .gpx file that you want to view"), f]), provider])
    return alt, f, gpd, provider, til


@app.cell
def _(alt, f, gpd, provider, til):
    try:
        gdf = gpd.read_file(f.contents(), layer="track_points")
    except Exception as e:
        m = til.create_tiles_chart(standalone=alt.Projection(type="mercator", scale=60_000, center=[52.0, 5.0])).properties(
            width=600, height=400
        )
    else:
        # GeoPandas creates a 'geometry' column with POINT objects.
        # For Altair to draw a connected line using mark_line(), it is easiest
        # to explicitly extract the Longitude (x) and Latitude (y) into their own columns.
        gdf["longitude"] = gdf.geometry.x
        gdf["latitude"] = gdf.geometry.y

        # --- 3. VISUALIZATION ---

        # Define the line chart
        # We use mark_line() to connect the points in the order they appear in the GDF
        track_chart = (
            alt.Chart(gdf)
            .mark_line(color="red", strokeWidth=3)
            .encode(
                longitude="longitude:Q",
                latitude="latitude:Q",
                # Add tooltips if the columns exist in your GPX
                tooltip=[
                    alt.Tooltip("time", title="Time", format="%H:%M:%S"),
                    alt.Tooltip("ele", title="Elevation (m)"),
                    alt.Tooltip("latitude", title="Lat"),
                    alt.Tooltip("longitude", title="Lon"),
                ],
            )
            .project(type="mercator")
        )

        m = til.add_tiles(track_chart, provider=provider.value).properties(width=600, height=400)
    return (m,)


@app.cell
def _(m):
    m
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
