{
  "old": "    if (uiAcc >= 0.25) { uiAcc = 0; updateUI(); }\n    onPointerCancel({pointerId:drag?.pointerId}); speed = 1; $('speedSelect').value = '1'; document.querySelector('.stage').classList.add('game-active');\n    if (g.over) { playing = false; showEnd(); }",
  "new": "    if (uiAcc >= 0.25) { uiAcc = 0; updateUI(); }\n    if (g.over) { playing = false; showEnd(); }"
}