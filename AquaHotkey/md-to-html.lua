function Link(el)
  el.target = string.gsub(el.target, "%.md", ".html")
  if string.find(el.target, "src") then
    el.target = string.gsub(el.target, ".*src", "https://github.com/0w0Demonic/AquaHotkey/blob/main/src")
  end
  return el
end
