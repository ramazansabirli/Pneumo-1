import plotly.graph_objects as go

def plot_shap_html(shap_values, feature_names, feature_values) -> str:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=shap_values,
        y=feature_names,
        orientation='h',
        marker=dict(
            color=['red' if val > 0 else 'blue' for val in shap_values],
            line=dict(color='black', width=1)
        )
    ))

    fig.update_layout(
        title="SHAP Özellik Katkıları",
        xaxis_title="Katkı",
        yaxis_title="Özellik",
        template="plotly_white"
    )

    return fig.to_html(full_html=False)
