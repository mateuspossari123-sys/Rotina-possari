// Cabeçalho e rodapé comuns a todas as telas da proposta.
(function () {
  var ativo = document.body.getAttribute('data-ativo') || '';
  var itens = [['inicio', 'Início', 'inicio.html'], ['sobre', 'A Comunidade', 'inicio.html#sobre'], ['formacao', 'Formação', 'formacao.html'], ['eventos', 'Eventos', 'evento.html'], ['noticias', 'Notícias', 'noticias.html'], ['oracao', 'Pedido de Oração', 'oracao.html']];
  var menu = itens.map(function (i) { return '<li><a class="' + (i[0] === ativo ? 'ativo' : '') + '" href="' + i[2] + '">' + i[1] + '</a></li>'; }).join('');
  document.body.insertAdjacentHTML('afterbegin',
    '<div class="topbar"><div class="wrap"><span>📍 Rua Spinard, 23 · Jd. Vera Cruz · Dracena-SP</span><span class="esc">WhatsApp <b>(18) 99670-8825</b> · <b>@sim_dracena</b></span></div></div>' +
    '<header class="nav"><div class="wrap"><a class="marca" href="inicio.html"><img src="../site/img/logo-sim.jpg" alt=""><span><b>Rede SIM</b><small>Irmãos da Misericórdia</small></span></a>' +
    '<ul class="menu">' + menu + '<li><a class="btn btn-ouro" href="contribua.html">Contribua</a></li></ul>' +
    '<span class="hamb"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span></div></header>');
  document.body.insertAdjacentHTML('beforeend',
    '<footer><div class="wrap"><div class="grade">' +
    '<div><a class="marca" href="inicio.html"><img src="../site/img/logo-sim.jpg" alt=""><span><b>Rede SIM</b><small>Irmãos da Misericórdia</small></span></a><p class="lema">Jesus, eu confio em vós!</p><div class="redes"><span>IG</span><span>YT</span><span>FB</span><span>WA</span></div></div>' +
    '<div><h4>A comunidade</h4><ul><li>Quem somos</li><li>Nossa história</li><li>Loja SIM</li><li>Contribua</li></ul></div>' +
    '<div><h4>Formação</h4><ul><li>Diga SIM a Deus</li><li>Santificai-vos</li><li>Grupo de Oração</li><li>Eventos</li></ul></div>' +
    '<div><h4>Contato</h4><ul><li>Rua Spinard, 23</li><li>Jd. Vera Cruz · Dracena-SP</li><li>(18) 99670-8825</li><li>@sim_dracena</li></ul></div>' +
    '</div><p class="copy">© 1996–2026 Sociedade Irmãos da Misericórdia</p></div></footer>');
  var t = document.body.getAttribute('data-tela');
  if (t) document.body.insertAdjacentHTML('beforeend', '<span class="tela">' + t + '</span>');
})();
