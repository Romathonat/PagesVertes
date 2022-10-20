# Les Pages Vertes wep app

Loading JSON files over the `file://` protocol falls foul of modern 
browsers' Cross-Origin Resource Sharing policies. So, start a local
webserver:

```shell
python -m http.server
```

Then visit localhost:8000.