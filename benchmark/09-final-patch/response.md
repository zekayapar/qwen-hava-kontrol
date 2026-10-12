{
  "replacements": [
    {
      "old": "    g = s; sel = null; last = 0; uiAcc = 0;\n    if (g.over)",
      "new": "    g = s; sel = null; last = 0; uiAcc = 0;\n    if (g.over) { onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; stage.classList.add('game-active'); }"
    },
    {
      "old": "      g = s; sel = null; last = 0; uiAcc = 0;\n      if (g.over)",
      "new": "      g = s; sel = null; last = 0; uiAcc = 0;\n      if (g.over) { onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; stage.classList.add('game-active'); }"
    },
    {
      "old": "  const rw = g.runways.find(r => r.accepts.includes(p.type) && !r.closed);",
      "new": "  const rw = g.runways.find(r => r.accepts.includes(p.type) && !r.closed && r.busy <= 0);"
    }
  ]
}