# blueprints

## create blueprint and register blueprint

```py
# create one
simple_bp = Blueprint('simple_page', __name__)

# register to app

app.register_blueprint(simple_bp)
```

## Blueprint Resources

### `static_folder`


## build url

url_for(endpoint)

## Error Handlers

`Blueprint`和`application`一样都支持`errorhandler`。

```py3
@simple_page.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html')
```

`errrohandler`只会被同`blueprint`下的`raise`和`abort`触发。
