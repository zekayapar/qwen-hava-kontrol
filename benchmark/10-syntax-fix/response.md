{
  "replacements": [
    {
      "old": "    if (g.over) { onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; stage.classList.add('game-active'); } {",
      "new": "    onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; document.querySelector('.stage').classList.add('game-active');\n    if (g.over)"
    },
    {
      "old": "      if (g.over) { onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; stage.classList.add('game-active'); } {",
      "new": "      onPointerCancel({pointerId:drag?.pointerId}); speed=1; $('speedSelect').value='1'; document.querySelector('.stage').classList.add('game-active');\n      if (g.over)"
    }
  ]
}