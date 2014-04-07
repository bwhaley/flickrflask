require("os")
local cjson = require "cjson"
 
local m = ngx.re.match(ngx.var.request, "/api/?search/(.*) ")
if m then
  local word = m[1]
  local res = ngx.location.capture("/v1/word/" .. word .. ".json")
  local value = cjson.new().decode(res.body)
  if value.sentiment < 5 then 
    local new_sentiment = value.sentiment + 1
    local res = ngx.location.capture("/v1/word/" .. word .. ".json?value=" .. new_sentiment, { method = ngx.HTTP_POST })
  end
else
  return
end



