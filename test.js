var checkUrl = require("./url_check")

suspect = ["wildunix.es", "www.wildunix.es", "http://wildunix.es", "https://wildunix.es", "http://wwww.wildunix.es", "https://www.wildunix.es",
          "https://d1f4470da51b49289906b3d6cbd65074@app.getsentry.com/13176", "mongodb://u:p@example.com:10064/db", "wss://secure.example.com/biz",
        "af", "", "http://dsfafasd"]
for (var i = 0; i < suspect.length; i++) {
  if (checkUrl(suspect[i])){
    console.log("yes")
  }else {
    console.log("no")
  }
}
