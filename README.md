## Dash PDF Generation Demo

> This documentation is for the [Dash Deployment Server](https://plot.ly/dash/pricing), Plotly's commercial platform for deploying and managing Dash applications. [View the docs](https://dash.plot.ly/dash-deployment-server/) or [request a trial](https://plotly.typeform.com/to/rkO85m).

This example provides a simple UI around the PDF API. You can run this example locally or you can deploy this example to Dash Deployment Server. A few things to note:
- Find your API key by visiting https://<your-plotly-server>/settings/api
- The username and API key are read from environment variables. [Learn how to set environment variables on Dash Deployment Server](https://dash.plot.ly/dash-deployment-server/environment-variables).

### Run Locally

To run this app locally follow the below:

```
git clone https://github.com/plotly/dash-pdf-generation-demo.git dash-pdf
cd dash-pdf

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

Then in `app.py` update:

- `PLOTLY_BASE_URL`https://github.com/plotly/dash-pdf-generation-demo/blob/master/app.py#L60
- `PLOTLY_USERNAME`https://github.com/plotly/dash-pdf-generation-demo/blob/master/app.py#L67
- `PLOTLY_API_KEY` https://github.com/plotly/dash-pdf-generation-demo/blob/master/app.py#L68

From the command line, run the application:

```
python app.py
```

and check http://127.0.0.1:8050/

### Deploy to Dash Deployment Server (DDS)

For information about how to deploy an application to the Dash Deployment Server, see our [DDS Documentation](https://dash.plot.ly/dash-deployment-server) 

### PDF API Parameters
```
POST https://<your-plotly-enterprise-server>/api/dash-apps/image
content-type: application/json
plotly-client-platform: dash
Authorization: Basic ...

{
    "url": "...",
    "pdf_options": {
        "pageSize": "Letter",
        "marginsType": 1
    },
    "wait_selector": "body"
}
```
- `url` - The URL to download
- `wait_selector` - A string that specifies a [CSS selector](https://developer.mozilla.org/en-US/docs/Learn/CSS/Introduction_to_CSS/Simple_selectors). The API will wait until an element that matches this CSS selector appears on the screen before taking a screenshot. This ensures that the page has finished loading before taking a screenshot. In general, we recommend:
    - If there are no graphs on the page, then embed an `html.Div(id='waitfor')` in your `app.layout` or return it from the callback that gets executed last. With the id `waitfor`, the `wait_selector` would be `"#waitfor"`.
    - If the page has `dcc.Graph` elements on it, then you'll want to wait until these graphs have finished renderering. To do this, set the `wait_selector` to be `#graph_id .svg-container` where `"graph_id"` corresponds to the ID of the `dcc.Graph` component. `.svg-container` refers to a CSS class of an element that plotly inserts in the graph when it has finished rendering.
- `pdf_options` - PDF sizing options. These options are similar to the options that you see when you print a web page using your web browser. They include:
    - `pageSize`: Page size of the generated PDF. Available options: `A3`, `A4`, `A5`, `Legal`, `Tabloid` or `{"width": ..., "height": ...}` where `width` and `height` are integers specified in microns.
    - `marginsType`: Specifies the type of margins to use. `0` for default margin, `1` for no margin, and `2` for minimum margin. We recommend using `1` and controlling the margins yourself through your app's CSS.
    - `landscape` (optional): `True` for landscape, `False` for portrait.
