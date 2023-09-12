
class WebPage:
    def head(self, title="Title"):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>%s</title>
    <style>
        body {
         text-align: left;
        }
        .tit {
         color: blue;
         font-size: 20px;
         font-family: sans-serif;
        }
        .txt {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            font-size: 12px;
        }
        .error {
            color: red;
            font-size: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
        }
   </style>
</head>
<body class="txt">
""" % title

