require("os")
local cjson = require "cjson"
 
local m = ngx.re.match(ngx.var.request, "/sentiment/(.*) ")
local res = ngx.location.capture("/v1/word/" .. m[1] .. ".json")
local value=cjson.new().encode(res.body)
ngx.say(res.body)

