%Identification
%%The class identifies itself and the LaTeX version needed
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{Academic}[2020/09/06 Made By Liam Hughes]
\LoadClass[twoside, a4paper, 12pt]{article} %changed to 12pt


%%Preliminary definitions, needed by the options
\newcommand{\headlinecolor}{\normalcolor}
\renewcommand{\familydefault}{\sfdefault}

\RequirePackage[table,xcdraw]{xcolor}
\definecolor{slcolor}{HTML}{882B21}

%%This parts handles the options passed to the class.
\DeclareOption{onecolumn}{\OptionNotUsed}
%\DeclareOption{onecolumn}{\onecolstyletrue}
\DeclareOption{green}{\renewcommand{\headlinecolor}{\color{green}}}
\DeclareOption{red}{\renewcommand{\headlinecolor}{\color{slcolor}}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

%twocolumn

%Packages
\RequirePackage{tikz}
\RequirePackage{kantlipsum}
\RequirePackage{lipsum}
\RequirePackage{amsmath, amsfonts, amssymb, bm}
\RequirePackage{setspace}
\RequirePackage{url}
\RequirePackage{graphicx}
\RequirePackage{adjustbox}
\RequirePackage{wrapfig}
\RequirePackage[UKenglish, nodayofweek]{datetime}
\RequirePackage{caption}
\RequirePackage{subcaption}

%Packages
\RequirePackage[percent]{overpic}
\RequirePackage[figuresright]{rotating}
\RequirePackage{pdfpages}
\RequirePackage{pdflscape}
\RequirePackage{siunitx}
\RequirePackage{xfrac}
\RequirePackage{asymptote}
\RequirePackage{mathrsfs}
\RequirePackage{afterpage}
\RequirePackage{changepage}
\RequirePackage{needspace, blindtext, changepage, setspace, float, placeins}
\RequirePackage[symbol, bottom]{footmisc}

\RequirePackage{appendix}
\RequirePackage{emptypage}
\RequirePackage{etoolbox}

\usepackage{booktabs}
\usepackage{ marvosym }

%Commands that are mine!
\newcommand{\vectg}[3]{$\text{\sfrac{#1}{#2}}  \text{$\langle$}#3\text{$\rangle$} $}
\newcommand{\dir}[1]{\text{$\langle$}#1\text{$\rangle$}}
\newcommand{\gantt}[1]{\hyperref[fig:Gantt]{#1}}
\newcommand{\vectbr}[3]{$\text{\sfrac{#1}{#2}}${[}$\text{#3}${]}}




%\sloppy - required if text falls off page
%\fussy - if you want to undo \sloppy

%Title modifications

%Paragraphs
\RequirePackage{indentfirst}
\setlength{\parindent}{3ex}
\setlength{\parskip}{0ex}

%Word Count
\newcommand{\quickwordcount}[1]{%
  \immediate\write18{texcount -1 -sum=1,0,0,0,0,0,0 -merge #1.tex > #1-words}%
  \input{#1-words}%
}
%\quickwordcount{main} - name of main.tex document (extension not required)
%counts (text words, header words, caption words, #headers, #floats, #inlined formulae, #displayed formulae) 


%colourbox
\newcommand\mybar{\kern1pt\rule[-\dp\strutbox]{1pt}{\baselineskip}\kern1pt}
\RequirePackage{color}
\definecolor{lightgray}{gray}{0.85}
\newcommand\greybox[1]{%
  \par\noindent\colorbox{lightgray}{%
    \begin{minipage}{\textwidth}#1\end{minipage}%
  }%
  \vskip\baselineskip%
}

%Main Title
\title{%
\vspace{-3.5em} %Move the image up the page
%\begin{centering}
%\end{centering}%

\begin{minipage}[l]{0.8\textwidth} %\vskip 0.5em
\textbf{\LARGE \myTitle}\\
\vspace{-0.5em}
\end{minipage}\hspace*{0.5cm}
\begin{minipage}[r]{0.155\textwidth}\vskip 0.5em
\hfill\includegraphics[width=\linewidth]{Images/logo.png}\\
\end{minipage}
%
}

\author{
\vspace{-2em}



\textbf{\MyAuthor$^{1}$
    }\\
    \small{$^{1}$\MyDepartment}
    %\small{$^{2}$Supervisor,}
    %\small{$^{3}$Co-Supervisor} Can add more names...
}


\RequirePackage{titling}
\pretitle{% add some rules
  \vskip 1.5em
    \huge\bfseries
    \begin{flushleft}
}%, make the fonts bigger, make the title (only) bold
\posttitle{%
  \end{flushleft}%
  %\noindent\vrule height 2.5pt width \textwidth
  %\vskip .75em plus .25em minus .25em%a increase the vertical spacing a bit, make this particular glue stretchier
}
\RequirePackage{microtype}
\newcommand{\Keywords}{Keyword1, keyword2, keyword3}
\newcommand{\myTitle}{Title}
\newcommand{\MyAuthor}{John J. Smith}
\newcommand{\MyDepartment}{Department}
\newcommand{\ID}{1234567}

\preauthor{%
    \vspace{0em}
    %\large
    \begin{flushleft}
    \vspace{0.0em}\Large %\bfseries %edit bold
}



\postauthor{%
    \end{flushleft}%
    \vskip 0em
    \vspace{0em}
    \noindent\textnormal{\quickwordcount{_main}Words} 
    \hfill \textls[20]{Student ID:\ID}\\
    \textls[45]{\textbf{Keywords:}} {\Keywords}
    \vspace{-0.8em} %change distance from
}

%Date Settings
\predate{
\hfill\begin{minipage}[t]{0.3\textwidth}\begin{flushright}\textls[10]{
}
\postdate{\end{flushright}\end{minipage}}}

%Custom Abstract
\RequirePackage{expl3,xparse,xcoffins}
\ExplSyntaxOn
\coffin_new:N \l_my_abstract_coffin %Ignore errors
\dim_zero_new:N \l_my_width_dim
\keys_define:nn { my / abstract }
  {
    width .code:n = {
      \dim_set:Nn \l_my_width_dim {#1\textwidth}
    }
  }

\NewDocumentCommand \myabstract { O {width=0.85} m }{%
  \keys_set:nn { my / abstract } { #1 }
  \SetVerticalCoffin \l_my_abstract_coffin {\l_my_width_dim} {#2}
  \renewcommand\maketitlehookd{%
  \noindent\rule{\textwidth}{1pt}\\
  
  %\section*{Abstract}
  %\text{Abstract}\\
  
    \mbox{}\medskip %\par
    \centering
    \TypesetCoffin \l_my_abstract_coffin\\
    \vspace{-2em}
    
    \noindent\rule{\textwidth}{1pt}
    
    \vspace{-1em} %move intro closer to abstract
  }

}
\ExplSyntaxOff


%Links and colours
\definecolor{azure}{rgb}{0.0, 0.5, 1.0}
\RequirePackage[bookmarks, hidelinks]{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=azure,
    filecolor=magenta,      
    urlcolor=azure,
    citecolor=azure,
    hypertexnames=true
}

%Margins and Columns
\RequirePackage[includeheadfoot,top=0.5in, bottom=0.5in, 
    left=1in, right=1in, headheight=15pt]{geometry} %chnaged to 15 for size 12pt font



\setlength{\columnsep}{10mm} %Column spacing

%Badness
\widowpenalty10000
\clubpenalty10000

\hbadness=999999
\vbadness=999999

% \showboxbreadth=50 
% \showboxdepth=50

%Strechpars for paragraph neatness
\newenvironment{stretchpars}
{\par\setlength{\parfillskip}{0pt}}
{\par}


\newenvironment{changemargin}[2]{%
\begin{list}{}{%
\setlength{\topsep}{0pt}%
\setlength{\leftmargin}{#1}%
\setlength{\rightmargin}{#2}%
\setlength{\listparindent}{\parindent}%
\setlength{\itemindent}{\parindent}%
\setlength{\parsep}{\parskip}%
}%
\item[]}{\end{list}}


%Section Style
 \RequirePackage[compact]{titlesec}
    \titlespacing{\section}{2pt}{2ex}{2ex}
    \titlespacing{\subsection}{1.5pt}{1.5ex}{1.5ex}
    \titlespacing{\subsubsection}{1pt}{1ex}{1ex}

\RequirePackage{titlesec, blindtext, color, tipa}
\newcommand{\hsp}{\hspace{20pt}}

\usetikzlibrary{positioning}
\RequirePackage[absolute,overlay]{textpos}

%Headings and Footers
\RequirePackage{lastpage}
\RequirePackage{fancyhdr}
%Title Page Heading
\fancypagestyle{plain}{%


  \fancyfoot[C]{}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
  \fancyhead[L]{}
  

 
  \fancyhead[C]{}
  \fancyhead[R]{}
  \fancyfoot[L]{}
}

%Fancy Headings
\pagestyle{fancy}
\fancyhead[RE,LO]{\slshape{\MyAuthor}}
% \fancyhead[C]{\leftmark}
\fancyfoot[C]{}
\fancyhead[RO,LE]{Page \thepage \hspace{1pt} of \hypersetup{linkcolor=black}{\pageref*{LastPage}}}
\renewcommand{\headrulewidth}{1pt} %0.5
\renewcommand{\footrulewidth}{0pt}


%Equation Style - Counters
%\renewcommand{\theequation}{\arabic{section}.\arabic{equation}}
%\counterwithin{figure}{section}
%\counterwithin{table}{section}



%Figures and Tables
\RequirePackage[compatibility=false,labelfont=it, singlelinecheck=false]{caption} %,textfont={bf,it}
\captionsetup{labelfont=bf} %textfont=bf
\renewcommand{\figurename}{Fig.}
\captionsetup[table]{labelformat=simple, labelsep=newline}
\captionsetup[figure]{labelformat=simple, labelsep=period}


%Use code inline
\RequirePackage{listings}

\RequirePackage[utf8]{inputenc}
\DeclareUnicodeCharacter{394}{$\Delta$}
\DeclareUnicodeCharacter{3008}{$\langle$}
\DeclareUnicodeCharacter{3009}{$\rangle$}


\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}
\lstset{style=mystyle}


%References 
\RequirePackage[style=nature, maxbibnames=99, doi=false,url=false,isbn=false,hyperref=true, backref=false, natbib=true, labelnumber]{biblatex}

%Add reference files!!!
\addbibresource{references.bib}