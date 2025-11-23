import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium", layout_file="layouts/gpx-on-folium.grid.json")


@app.cell
def _():
    import geopandas as gpd
    import folium
    from folium.plugins import MousePosition
    import marimo as mo


    f = mo.ui.file(filetypes=[".gpx"], multiple=False)
    mo.vstack([mo.md("Please upload a .gpx file that you want to view"), f])
    return MousePosition, f, folium, gpd


@app.cell(hide_code=True)
def _(MousePosition, f, folium, gpd):
    map_start_zoom = 13

    # --- 2. DATA LOAD ---
    try:
        # Load the track points layer to get individual data points
        gdf = gpd.read_file(f.contents(), layer="track_points")
    except Exception as e:
        # print(f"Error loading GPX file: {e}")
        m = folium.Map()
    else:
        # Drop rows where elevation or geometry might be missing (optional cleanup)
        gdf = gdf.dropna(subset=["geometry"])

        # Folium requires coordinates in (Latitude, Longitude) format.
        # GeoPandas/Shapely stores them as (Longitude, Latitude).
        # We extract them into a list of tuples: [(lat, lon), (lat, lon), ...]
        track_coordinates = [(point.y, point.x) for point in gdf.geometry]


        # Initialize the map centered on the starting point of the track
        start_coords = track_coordinates[0]
        m = folium.Map(location=start_coords, zoom_start=map_start_zoom, tiles="Cartodb Positron")

        # A. Draw the Track Line
        folium.PolyLine(locations=track_coordinates, color="red", weight=4, opacity=0.8, tooltip="GPX Track").add_to(m)

        # B. Add Start and End Markers (Green and Red)
        # Start
        folium.Marker(location=track_coordinates[0], popup="Start", icon=folium.Icon(color="green", icon="play")).add_to(m)

        # End
        folium.Marker(location=track_coordinates[-1], popup="End", icon=folium.Icon(color="red", icon="stop")).add_to(m)

        # C. Automatically fit the map bounds to the track
        m.fit_bounds(m.get_bounds())
        MousePosition().add_to(m)
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
