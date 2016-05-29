set background=dark
highlight clear

if exists("syntax on")
    syntax reset
endif

set number

hi Normal    ctermbg=8 ctermfg=15
hi ErrorMsg  ctermbg=1 ctermfg=15
hi Visual    ctermbg=7 ctermfg=8
hi VisualNOS ctermbg=8 ctermfg=8
hi Todo      ctermbg=8 ctermfg=13
hi Search    ctermbg=8 ctermfg=8
hi IncSearch ctermbg=8 ctermfg=8

hi SpecialKey ctermbg=8 ctermfg=8
hi Directory  ctermbg=8 ctermfg=8
hi Title      ctermbg=8 ctermfg=15
hi WarningMsg ctermbg=8 ctermfg=8
hi ModeMsg    ctermbg=8 ctermfg=8
hi MoreMsg    ctermbg=8 ctermfg=8
hi Question   ctermbg=8 ctermfg=8
hi NonText    ctermbg=8 ctermfg=8

hi StatusLine   ctermbg=8 ctermfg=15
hi StatusLineNC ctermbg=8 ctermfg=15
hi VertSplit    ctermbg=8 ctermfg=7

hi Folded       ctermbg=8 ctermfg=8
hi FoldedColumn ctermbg=8 ctermfg=8
hi LineNr       ctermbg=8 ctermfg=7

hi DiffAdd    ctermbg=8 ctermfg=10
hi DiffChange ctermbg=8 ctermfg=6
hi DiffDelete ctermbg=8 ctermfg=9
hi DiffText   ctermbg=8 ctermfg=3

hi Cursor  ctermbg=8 ctermfg=15
hi lCursor ctermbg=8 ctermfg=8

hi Comment    ctermbg=8 ctermfg=7
hi Constant   ctermbg=8 ctermfg=9
hi Special    ctermbg=8 ctermfg=11
hi Identifier ctermbg=8 ctermfg=2
hi Statement  ctermbg=8 ctermfg=6
hi PreProc    ctermbg=8 ctermfg=14
hi type       ctermbg=8 ctermfg=3
hi Underlined ctermbg=8 ctermfg=5
hi Ignore     ctermbg=8 ctermfg=7
