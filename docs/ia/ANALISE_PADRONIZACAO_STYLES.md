# Análise de Padronização de Styles - Perguntas Estratégicas

**Data:** 8 de março de 2026  
**Objetivo:** Estabelecer padrão unificado de estilos em todas as classes de widgets

---

## 📊 Análise Atual

### Widgets Encontrados (10 classes):
1. **AppBarWidget** - Barra superior com título + botões
2. **AttributeSelectorWidget** - Seleção de atributos/campos
3. **BottomActionButtonsWidget** - Botões inferiores (Run/Close/Info)
4. **CollapsibleParametersWidget** - Seção expansível de parâmetros
5. **FileSelectorWidget** - Seletor de arquivo único
6. **LayerInputWidget** - Seletor de camada (QgsMapLayerComboBox)
7. **MainLayout** - Layout principal do dialog
8. **PathSelectorWidget** - Seletor de pasta/arquivos (novo, refatorado)
9. **RadioButtonGridWidget** - Grid de radio buttons exclusivos
10. **ScrollWidget** - QScrollArea customizada com tema

### Estilos Atuais (Styles.py):
- **Cores base:** PRIMARY (#a6784f), TEXT_PRIMARY, BACKGROUND, BORDER
- **Fontes:** FONT_FAMILY_DEFAULT, FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL
- **Spacing:** ITEM_HEIGHT, LAYOUT_V_SPACING, LAYOUT_H_SPACING, CONTENT_PADDING
- **Métodos:** main_application(), buttons(), scroll_area(), collapsible_parameters(), etc

### Problema Identificado:
- ✅ Spacing padrão está OK (12px itens, 2px spacing vertical)
- ❌ **Widgets usam QWidget.setStyleSheet() MANUALMENTE**
- ❌ **Não há método unificado em Styles para cada widget type**
- ❌ **Cores, fontes e tamanhos não aplicados consistentemente**
- ❌ **ObjectNames definidos em widgets mas Styles.py não os estiliza**

---

## 🎯 PERGUNTAS PARA VOCÊ RESPONDER

### Bloco 1: Arquitetura de Styling

**P1.1:** Como você quer que os estilos sejam aplicados?
- **Opção A:** Via `setStyleSheet()` em cada widget (cada widget chama `Styles.widget_type()`)
- **Opção B:** Via arquivo .qss externo centralizado (melhor para temas)
- **Opção C:** Híbrido (arquivo .qss base + overrides programáticos para cores dinâmicas)
- **Sua escolha:** ___________

**P1.2:** Quem deve ser responsável por aplicar estilos?
- **Opção A:** Cada widget aplica seu próprio estilo no __init__
- **Opção B:** WidgetFactory aplica após criar o widget
- **Opção C:** BasePlugin aplica em _build_ui()
- **Sua escolha:** ___________

---

### Bloco 2: Estrutura de Cores

**P2.1:** Paleta de cores - você quer:
- **Opção A:** Cores separadas por tipo de elemento (buttons, labels, inputs, etc)
- **Opção B:** Cores por estado (normal, hover, pressed, disabled, focused)
- **Opção C:** Ambas + variações de tema (escuro, claro)
- **Sua escolha:** ___________

**P2.2:** O #a6784f (COLOR_PRIMARY marrom) deve ser usado em:
- **Opção A:** Somente em elementos críticos (buttons, borders, headers)
- **Opção B:** Em todo lugar para consistência visual (buttons, hovers, focus states, etc)
- **Opção C:** Apenas como acentuação (hover states, borders, selected items)
- **Sua escolha:** ___________

**P2.3:** Fundo e texto - padrão para **TODOS** os widgets:
- **Opção A:** Background = COLOR_BACKGROUND_PANEL (rgb 34,30,26), Text = COLOR_TEXT_PRIMARY
- **Opção B:** Herdar do sistema (deixar transparente)
- **Opção C:** Diferente para cada tipo (inputs com fundo mais claro, labels transparentes)
- **Sua escolha:** ___________

---

### Bloco 3: Tamanhos e Padding

**P3.1:** QLineEdit / QComboBox / inputs genéricos:
- **Opção A:** Altura fixa 24px (já está sendo feito em PathSelectorWidget)
- **Opção B:** Altura mínima 28px (um pouco maior)
- **Opção C:** Altura 24px + padding interno padrão
- **Sua escolha:** ___________

**P3.2:** Botões (QPushButton):
- **Opção A:** Altura = ITEM_HEIGHT (12px) - muito pequeno, seria mínimo
- **Opção B:** Altura fixa 24px (mesmo que inputs)
- **Opção C:** Altura 32px (mais generoso)
- **Sua escolha:** ___________

**P3.3:** Checkboxes / RadioButtons:
- **Opção A:** Tamanho padrão do sistema (não forçar)
- **Opção B:** Tamanho fixo 16x16px
- **Opção C:** Tamanho fixo 20x20px
- **Sua escolha:** ___________

**P3.4:** Padding interno em widgets (margins):
- **Opção A:** Uniforme 4px em todos os lados
- **Opção B:** Diferente para horizontal (8px) vs vertical (4px)
- **Opção C:** Diferente por tipo de widget
- **Sua escolha:** ___________

---

### Bloco 4: Tipografia

**P4.1:** Font da aplicação inteira:
- **Opção A:** Manter 'Segoe UI' 9pt
- **Opção B:** Mudar para 'Roboto' 10pt (mais moderno)
- **Opção C:** Sistema padrão do Windows/Linux
- **Sua escolha:** ___________

**P4.2:** Tamanhos de fonte - você quer:
- **Opção A:** Apenas 3 tamanhos (TITLE=20pt, NORMAL=9pt, SMALL=8pt)
- **Opção B:** 5 tamanhos (TITLE=18pt, LARGE=11pt, NORMAL=9pt, SMALL=8pt, TINY=7pt)
- **Opção C:** Variável por contexto (labels, inputs, botões podem ter tamanhos diferentes)
- **Sua escolha:** ___________

**P4.3:** QLabel (rótulos):
- **Opção A:** COLOR_TEXT_SECONDARY (cinza claro #d2bca6)
- **Opção B:** COLOR_TEXT_PRIMARY (branco #ece6df)
- **Opção C:** Cinza mais escuro para melhor contraste
- **Sua escolha:** ___________

---

### Bloco 5: Estados (Hover, Focus, Disabled)

**P5.1:** Estados de botão:
- **Opção A:** Normal (primary color), Hover (lighter), Pressed (darker), Disabled (gray)
- **Opção B:** Apenas estado selecionado/deselecionado
- **Opção C:** Visual mínimo (apenas hover em cor clara)
- **Sua escolha:** ___________

**P5.2:** Inputs (QLineEdit, QComboBox):
- **Opção A:** Border normal 1px, Focus border 2px com PRIMARY color
- **Opção B:** Border normal transparent, Focus background alterado
- **Opção C:** Apenas background alterado em focus
- **Sua escolha:** ___________

**P5.3:** Disabled (widgets desabilitados):
- **Opção A:** Opacidade reduzida (70%)
- **Opção B:** Cor cinza desaturada
- **Opção C:** Ambas + texto mais claro
- **Sua escolha:** ___________

---

### Bloco 6: Bordas e Separadores

**P6.1:** Bordas em geral:
- **Opção A:** COLOR_BORDER (#a6784f marrom) 1px
- **Opção B:** Sem bordas (apenas fundo diferente)
- **Opção C:** Bordas sutis (cinza escuro) 1px
- **Sua escolha:** ___________

**P6.2:** Separadores (QFrame com HLine):
- **Opção A:** Cor = COLOR_BORDER 1px altura
- **Opção B:** Cor = COLOR_BORDER 2px altura
- **Opção C:** Cor mais clara (COLOR_TEXT_SECONDARY) 1px
- **Sua escolha:** ___________

---

### Bloco 7: Scrollbars

**P7.1:** ScrollWidget.scroll_area() - scrollbars:
- **Opção A:** Manter atual (COLOR_PRIMARY com hover/pressed states)
- **Opção B:** Scrollbars mais minimalistas (cinza claro apenas)
- **Opção C:** Scrollbars invisíveis até hover (desaparecem quando não usado)
- **Sua escolha:** ___________

---

### Bloco 8: Organização de Métodos em Styles.py

**P8.1:** Organização desejada:
```python
# Proposta atual:
Styles.main_application()        # Frame principal
Styles.buttons()                 # QPushButton
Styles.scroll_area()             # QScrollArea
Styles.collapsible_parameters()  # CollapsibleParametersWidget

# Você quer adicionar:
# Opção A - Métodos por tipo de widget:
Styles.line_edit()               # QLineEdit
Styles.combo_box()               # QComboBox
Styles.checkbox()                # QCheckBox
Styles.radio_button()            # QRadioButton
Styles.label()                   # QLabel
Styles.frame()                   # QFrame
Styles.app_bar()                 # AppBarWidget

# Opção B - Métodos por componente (wrapper de vários widgets):
Styles.input_field()             # QLineEdit + QComboBox
Styles.layer_selector()          # LayerInputWidget
Styles.path_selector()           # PathSelectorWidget
Styles.collapsible()             # CollapsibleParametersWidget

# Opção C - Híbrido (ambas as abordagens)
```
**Sua escolha:** ___________

**P8.2:** Cada método deve retornar:
- **Opção A:** String QSS pura (ex: `return "QPushButton { ... }"`)
- **Opção B:** Dicionário com componentes (border, background, color separados)
- **Opção C:** Ambas (método + método_dict para flexibilidade)
- **Sua escolha:** ___________

---

### Bloco 9: Temas Dinâmicos

**P9.1:** Suporte a múltiplos temas:
- **Opção A:** Apenas tema escuro atual (fixo)
- **Opção B:** Tema escuro + tema claro (selectable)
- **Opção C:** Tema customizável via arquivo de configuração
- **Sua escolha:** ___________

---

### Bloco 10: Aplicação Prática

**P10.1:** Qual widget você quer que eu padronize PRIMEIRO?
```
1. AppBarWidget - Barra superior
2. PathSelectorWidget - Já refatorado, mas precisa estilos
3. AttributeSelectorWidget - Seleção de campos
4. Todos widgets de input (QLineEdit, QComboBox, etc)
5. Todos simultaneamente
```
**Sua escolha:** ___________

**P10.2:** Você quer validação durante implementação?
- **Opção A:** Sim, validar via screenshot/print de como fica
- **Opção B:** Não, apenas implementar confiando na estrutura
- **Opção C:** Sim, mas com amostra de 2-3 widgets antes de aplicar ao resto
- **Sua escolha:** ___________

---

## 📝 Resumo do Que Preciso Fazer Após Respostas:

1. **Criar estrutura em Styles.py:**
   - Adicionar constantes de cores por elemento/estado
   - Criar métodos retornando QSS formatado
   - Implementar tema unificado

2. **Aplicar em widgets:**
   - Cada widget chama `self.setStyleSheet(Styles.widget_type())`
   - Ou aplicar via WidgetFactory
   - Testar visualmente

3. **Validar:**
   - Consistência visual em todos os plugins
   - Responsividade (hover, focus, disabled)
   - Compatibilidade com tema escuro

---

## 📌 Próximos Passos:

1. ✍️ **Você responde as 10 perguntas/blocos acima**
2. 🤖 **Eu estruturo Styles.py completo**
3. 🔧 **Eu aplico em todos os 10 widgets**
4. ✅ **Validamos visualmente**

**Aguardando respostas!**
