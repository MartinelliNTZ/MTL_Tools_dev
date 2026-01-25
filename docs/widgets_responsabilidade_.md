# Arquitetura de UI — Responsabilidades e Papéis

Este documento define, de forma **normativa**, as responsabilidades de cada camada envolvida na criação e uso de widgets nos plugins.  
O objetivo é garantir **padronização, independência, baixo acoplamento e escalabilidade**, eliminando camadas desnecessárias.

---

## 1. Widget Exclusivo (Componente de UI)

### Definição
Um **Widget Exclusivo** é uma unidade de UI **autossuficiente**, reutilizável e coesa.  
Sempre que um widget ou conjunto de widgets possuir **complexidade visual ou comportamental**, ele **deve** ser promovido a uma classe exclusiva.

### Responsabilidades
- Criar **todos os seus sub-widgets**
- Definir **seu próprio layout**
- Implementar **toda a lógica de interação**
- Manter **estado interno**
- Expor uma **API pública clara, pequena e orientada ao domínio**
- Ser **independente da Factory, Styles e Plugin**
- Poder ser reutilizado em qualquer contexto sem adaptações

### Não é responsabilidade do Widget Exclusivo
- Aplicar estilos globais
- Conhecer padrões visuais do projeto
- Conhecer o plugin que o utiliza

### Regra de ouro
> Se um widget ou conjunto possuir lógica própria, ele **deve** ser uma classe exclusiva.

---

## 2. WidgetFactory

### Definição
A **WidgetFactory** é responsável exclusivamente por **instanciar widgets** e **aplicar padronização visual**.

### Responsabilidades
- Instanciar widgets exclusivos
- Aplicar estilos padronizados
- Aplicar configurações visuais globais
- Centralizar a criação de componentes padronizados
- Retornar widgets prontos para uso

### Não é responsabilidade da Factory
- Implementar lógica de interação
- Manter estado dos widgets após criação
- Expor métodos comportamentais
- Orquestrar comunicação entre widgets

### Regra de ouro
> A Factory **cria e padroniza**, mas **não controla** o comportamento do widget.

---

## 3. Styles

### Definição
A camada de **Styles** define a **aparência visual** dos widgets de forma centralizada e reutilizável.

### Responsabilidades
- Definir cores, fontes, margens e espaçamentos
- Padronizar estados visuais (hover, disabled, active)
- Aplicar estilos por tipo de widget ou componente
- Conter estilos específicos apenas quando necessário

### Estrutura recomendada
- Estilos base (globais)
- Estilos por tipo de widget
- Estilos específicos para componentes complexos

### Não é responsabilidade dos Styles
- Criar widgets
- Implementar lógica
- Conhecer plugins ou fluxo de dados

### Regra de ouro
> Estilo é aparência, nunca comportamento.

---

## 4. Plugin (Genérico)

### Definição
O **Plugin** é o orquestrador da aplicação.  
Ele consome componentes de UI e conecta esses componentes à lógica de domínio.

### Responsabilidades
- Solicitar widgets à Factory
- Organizar widgets em layouts maiores
- Conectar widgets à lógica de negócio
- Consumir dados através da API pública dos widgets
- Controlar fluxo de execução (executar, salvar, carregar, etc.)

### Não é responsabilidade do Plugin
- Criar widgets manualmente
- Aplicar estilos
- Implementar lógica interna de UI
- Conhecer sub-widgets ou estrutura interna

### Regra de ouro
> O plugin **orquestra**, mas **não constrói nem detalha a UI**.

---

## 5. Resumo Estrutural

Plugin
└── WidgetFactory
└── Widget Exclusivo
├── Sub-widgets
├── Layout
├── Lógica interna
└── API pública

- O plugin conversa com a Factory **apenas para criação**
- O plugin conversa com o Widget **apenas pela API pública**
- Widgets complexos **sempre** viram classes exclusivas
- Styles são aplicados exclusivamente pela Factory

---

## 6. Princípio Final

> **Factory cria e padroniza.  
> Widget é autônomo e encapsulado.  
> Styles definem aparência.  
> Plugin apenas orquestra.**

Este modelo garante clareza arquitetural, reutilização real e evita a introdução de camadas artificiais sem responsabilidade clara.
