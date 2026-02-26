
Skip To Content
Dashboard
Ahilan Kumaresan
Account
Dashboard
Courses
Groups
Calendar
One unread message.1
Inbox
History
Help
PHYS332W LA01PagesGuidelines for Your Formal Reports
Spring 2026
Home
Announcements
Modules
Assignments
Discussions
Files
Grades
People
Syllabus
Quizzes
Collaborations
Library Reserves
Course Experience Surveys
Guidelines for Your Formal Reports

Overview

Structure

Writing Strategies

LaTeX

Form

Fitting curves to data

Figures

Common Errors

Overview
Your formal report should be written in the format of a typical research article. Although a glance through different scientific journals will show that formats vary considerably, many features are common. 

Please refer to the material presented in class for general information about typical structure, and what to include in each section. In this document, we'll provide some pointers about specific issues.

Each of you is responsible for your own formal report, including analysis and figures. You can work with your partner on this, but make sure you are able to produce your own, independent versions.

Return to top

Details
Check out our example report Download example report.

The document begins with a Title. The title should be concise, but informative. Ideally, it should identify the field of study and your contribution.

You then summarize your work with an Abstract. This should be short (one paragraph) and summarize the experiment and results in mostly qualitative terms, so that someone who is not going to read the rest of the paper has an idea of what it is about. Usually, you do not include numbers in the abstract, unless the whole point of the experiment was to measure a specific number. (For example, if the experiment was to measure the gravitational constant 
, then it would be appropriate to give the value you determined. Usually though, that's better left for the paper itself.) A starting point is a sentence that describes each of the main sections of the paper. Another way to approach this is to make sure that the abstract addresses these questions: what you did, how you did it, and what you found. The title and abstract should stand on their own as a summary of the paper; in fact, searchable online databases usually contain only the title and abstract. One piece of advice - leave writing the abstract until you have finished the main body of the paper.

The first section of the paper proper is usually the Introduction. The general purpose of the introduction is to convince your audience that your project is scientifically interesting and worth reading about. A good introduction typically does 3 things: (1) provides contextual or background information, (2) identifies a gap in the knowledge e.g. an unresolved controversy, an untested or unproven hypothesis, an absence of data, etc., and (3) states the authors' contribution to this problem. It should also give an outline of what you will write about later on. This is not a strict formula for an introduction, but can be a good model to work from. Aim for 3-4 paragraphs written in non-technical style so that it is accessible to the general reader. Generally, there are no equations or figures in the introduction.

Note that there is no unique way of providing background information, because the method you choose should depend on your audience. For example, an article on an interference device applied to measuring spectra might be addressed to chemists primarily interested in spectroscopy, to engineers primarily interested in instruments, or to physicists interested in issues in optics. Each of these audiences would need its own particular style of introduction.

It is sometimes difficult, when presenting results from undergraduate experiments, to address point (2) above. At this stage you may find it easier to describe your work as confirming or testing rather than discovering.

The next section is usually a Theory section, where you give an overview of the theoretical context of your experiment. In general, you do not want the section cluttered with unnecessary equations. (But you don't want to leave out necessary ones!) If something is derived in one of your references, just give the reference and quote the result. If you need a non-standard result, you should derive it. If the derivation is short, leave it in the theory section. If it is long, put it in an appendix.

Next, the Methods section. Here, you describe your own apparatus and methods. The purpose of this section is two-fold: (1) to allow others to repeat your experiment in full or in part and (2) to convince your readers that your experimental design is sound and that your results are therefore valid. This section will be the most technical, but should be clear enough that the general reader can appreciate the experimental design. Add drawings or figures to help make the apparatus and methods accessible.

Finally you can present and discuss your results. This part of your report can be presented either as two sections (Results and Discussion) or as a single section (Results and Discussion) covering both aspects. Results should be presented as clearly and objectively as possible. In an experimental paper, the Results section will include figures showing representative data and fits. But it is not just a collection of figures; each figure should be introduced and described in the text. The presentation of results can be as important as the results themselves. The role of the Discussion is to be persuasive - to convince the reader of the significance. The Discussion includes an interpretation of the results as well as comparison with your expectations (e.g., hypothesis, model, theorem), or with other published work. It will probably include additional figures that support your arguments.

Finish your report with the Conclusions. Summarize the results and their importance in plain language, so that they are accessible to a broad audience.

The conclusions should be followed by Acknowledgements, where you should acknowledge your labmates, and References.

Return to top

Writing Strategies
This is a writing assignment, so here are a few writing strategies:

Before you start writing, do the following:
Anticipate your audience. Identifying your target audience will help you make decisions about how much background you need to provide and what sort of language to use. For this report, assume that your target audience is a fellow student, who has not yet done the experiment.
Define your purpose. It is not enough to simply present data - you should have a clear idea of what you want your readers to do with the data or take away from your paper. Ideally, you should be able to express the purpose of your paper in a sentence or two. This will help you organize your manuscript.
We recommend that you start with your figures. They will tell the story of your experiment. Build the Results and Discussion sections around the figures. The Theory and Experiment sections should be fairly straight forward as they are basically summarizing facts. But be sure that the Theory section is not just a list of equations, but that the physical meaning is clear. Leave the abstract and conclusion until last.
With the formal report, you will be expected to revise the report to take into account the comments we make. 
If English is not your native language (and even if it is!), use a spelling checker (and a dictionary when in doubt). Grammar and style checkers are also available but tend to be unreliable. Have a friend edit your report. SFU has resources for non-native English speakers as well - ask us for more information.
Do not be afraid to use the active voice. While passive constructions are sometimes useful, they are weaker and usually less effective than active ones. Some ways to use the active voice: use "I'' or "we'' (as the case may be). Use the imperative (eg,"
`one'' as a subject (careful: this can lead to stiff sounding phrases). Whichever voice you choose, make sure to be consistent within sections.
Written English is not the same as spoken English, and informal expressions and usages that are acceptable in the latter are often inappropriate in the former. For example, do not use contractions (eg, 
don't'' for 
do not''); do not use 
so'' as a conjunction. On the other hand, written English does not have to be awkward or boring. Try to write an interesting paper that you could imagine a fellow student enjoying.
Return to top

LaTeX
Check out the LaTeX quick-start page for help with LaTeX.
Use the formal report template Download formal report template!!!!
The tilde (~) character is understood by LaTeX as a non-breaking space. Make sure to include it between measurement values and their units, as in "12~cm." This will prevent LaTeX from breaking a line between "12" and "cm". Use non-breaking spaces also for "Fig.~1," "Eq.~(2)," and "Ref.~[3]."
When you refer to a numbered equation or figure at the beginning of a sentence, write out "Figure" or "Equation" without abbreviation. Otherwise, abbreviate them as "Fig." and "Eq." For example, "Figure~1 shows data together with a fit to Eq.~(2)." (Note that the "~" characters here indicate non-breaking spaces, as described above.)
Writing $sin\theta$ causes the sine function to be written in italics, 
, instead of in roman font, 
. Write $\sin\theta$ instead, to indicate that LaTeX should treat \sin as the sine function. Otherwise LaTeX treats s, i, and n as separate variables, so the function name appears in italics and with a letter spacing that is different from regular text. A list of similar functions is available in Table 181, p. 89, of the Comprehensive LaTeX Symbol ListLinks to an external site..
Similarly, any text that you write in LaTeX math mode will be understood as a mathematical expression. If you want to write text expression without leaving math mode, include the line \usepackage{amsmath} in the preamble, then use the \text command. For example, Newton's constant may be written as $G \approx 6.674 \times 10^{-11}~\text{m}^3\,\text{kg}^{-1}\,\text{s}^{-2}$, which will be parsed by LaTeX as 
. (Note that the "\," commands insert a thin space.)
Italicize fundamental constants like c, me, qe, etc.
Always use math mode to represent mathematical variables, eg, "temperature $T$", not "temperature T."
Use the 
 symbol ("\times" in LaTeX) when expressing powers of ten, not asterisks, dots, or "E" notation (ie, 3.2e-3).
LaTeX uses distinct symbols to open and close quotations. For double quotes, use 
'', and for single quotes use `'. Note that the double-quote marks include four distinct characters, or two copies each of ` and '.
Return to top

Form

A few issues about form:


Symbols (mathematical and physical) should be put in italics in the text and in display equations. For example, you might want to write about the electric field 
, which should be italicized, as should a reference to a particle's position 
.
Equations should all be numbered, and the numbers should be sequential for relatively short papers, such as your reports. (In other words, there should be no need to break down the equations by section, as you might do in a book or very long report.)
Diagrams and graphs should be presented as figures, with figure captions. They need to be numbered sequentially, and referred to by number in the text. Drawings of the experimental apparatus should ideally be done with a computer drawing program. If none is available or if it would be too difficult, do a hand drawing but then scan the image. That way, your entire report will be storable on computer. This will be useful for revising and printing your second draft, if nothing else.
References should be numbered. In the text, you refer to the reference by including the bracketed number at the end of the sentence where the reference is used. The format is like this [1]. (Here, we mean that in reference [1], one will find something that supports the sentence in which the reference occurs.) Numbering should be sequential through the text.
The actual information about the reference should be placed in a section entitled References, typically placed after the Conclusions and before any Appendices. The number of the reference should correspond to the number you used in the text.
We do not care about the exact style you use for your references, as long as you are consistent. Here are a couple of sample references, one for a journal article, and one for a book:
[1] T. B. Benjamin and F. Ursell, "The stability of the plane free surface of a liquid in vertical periodic motion,'' Proc. R. Soc. Lond. A 225, 505-515 (1954).
[2] D. J. Tritton, Physical Fluid Dynamics, 2nd. ed. (Oxford Univ. Press, Oxford, 1988), 101-132.
Note that in the above format, volume numbers are given in bold face and the familiar 
pp.'' for 
pages'' is omitted. The book reference also includes page numbers. Some journals allow one to omit the title and last page of the article, but you should include this information in your bibliography for student papers and theses.

A point about sources -- you generally should steer clear of web references. Wikipedia is not a reference! Also, avoid using the labscript as a reference - this is not a peer-reviewed or edited document. It is a summary of the references provided for that lab, and is just meant to get you started.


Make your own diagrams for the formal report. It is ok in some cases to use someone else's figure, as long as you give credit in the figure caption (by giving the reference number). Generally you do this when you are reproducing their data, for example. In the 
real world,'' you would normally also have to write the publisher, and perhaps the author, to get permission to use a figure. We won't be so sticky here!

Return to top

Fitting curves to data
Check out our data analysis resources.
All standard curve fitting software assumes that the uncertainty is in the y-variable. Consequently, if you want to estimate the parameters 
 and 
 in the relationship 
 but have noisy measurements of 
 and relatively precise measurements of 
 you must rearrange the expression in the form 
 to perform the fit and convert back to the original relationship using 
 and 
 Use error propagation to determine their uncertainties. 
Return to top

Figures
See the general guidelines on graphing your results for advice on formatting your figures
Use EPS format for line-art figures.
Format your plots so that when they are resized in your summary, the smallest letter in the plot is at least as large as a subscripted character in the text.
Do not include titles for figures in a report. Do include titles for figures in your notebook.
Return to top

Common Errors
Finally, here is a list of common errors in formal reports:

No abstract
Abstract is not self-contained. Do not refer to figures, etc., in the abstract.
Grandiose and irrelevant introductions. (
Since the dawn of time, man has been interested in the properties of light.'')
Missing references. References not referred to in text.
Figures, tables not numbered.
No captions for figures, tables.
Captions not detailed enough for the figure to be 'read' on its own.
Text in included graphics is too small (usually this occurs because the figure is reduced from its original size).
No reference to figures, and/or tables in text.
Equations not numbered.
Symbols in equations not defined.
Axes of graphs not labeled; units of quantities omitted
Data points on graphs not prominent. When presenting data and a curve fit, use symbols for the data points (not connected) and a solid line for the fit function. Evaluate your fit function over a large enough set of points to obtain a smooth curve. Do NOT evaluate it only on the 
-values corresponding to data points unless there are lots of points. 
No error bars on graphs. (If the errors are so small that bars do not show, say this.)
No indication of how error estimates were obtained; no mention of the most important contributions to the error in a measurement.
No consideration of possible systematic errors.
Calling experimental constants (such as "
'') the "theoretical'' value.
Return to top




Skip To Content
Dashboard
Ahilan Kumaresan
Account
Dashboard
Courses
Groups
Calendar
One unread message.1
Inbox
History
Help
PHYS332W LA01PagesWriting
Spring 2026
Home
Announcements
Modules
Assignments
Discussions
Files
Grades
People
Syllabus
Quizzes
Collaborations
Library Reserves
Course Experience Surveys
Writing
Assignments
LaTeX Template for skeleton draft Download skeleton draft  and formal reportDownload formal report
The sample formal report can be used as a template for assignments, as well.
Schedule Download Scheduleand guidelines for the formal report
Examples
We will base the writing lectures and assignments (mostly) on
T. Li, S. Kheifets, D. Medellin, and M. G. Raizen, Science 328, 1673–1675 (2010) Download T. Li, S. Kheifets, D. Medellin, and M. G. Raizen, Science 328, 1673–1675 (2010). 

This article follows the classic style very closely:  A. J. Cox et al., Am. J. Phys. (2002)Download A. J. Cox et al., Am. J. Phys. (2002)
This article is written in a "letter" style:  M. Ahmadi et al., Nature (2017)Download M. Ahmadi et al., Nature (2017)
Decent examples of figures, captions, equations, methods:   Y. Deng et al., J. Opt. A (2007)Download Y. Deng et al., J. Opt. A (2007)

Scientific Document Preparation
For this course, we require you to use LaTeX to prepare your scientific documents.  There is a learning curve, but the final output is superior.  LaTeX resources can be found in our  LaTeX Quick Start guide.

General LaTeX Information
Getting started with LaTeX: LaTeX Quick Start

Using RevTex:  APS RevTex 4.2 Author's GuideDownload APS RevTex 4.2 Author's Guide

Physics style guide:  Physical Review Style and Notation GuideDownload Physical Review Style and Notation Guide

NIST guidelines for typesetting mathematicsLinks to an external site.; see also notes by HighamLinks to an external site.

Technical Writing Resources
Joseph E. Harmon and Alan G. Gross, The Craft of Scientific CommunicationLinks to an external site.. , 3rd ed. The University of Chicago Press, 2010.  
— available online from the SFU library (with restrictions on use).
— this will be our main reference for the writing lectures.  Good, but written by authors who seem never to have heard about theory or equations....
Michael Alley, The Craft of Scientific WritingLinks to an external site., 4th ed., Springer (2018).  Available as a pdf download from SFU library.
— written by an engineer.
Randy Olson, Houston, We Have a NarrativeLinks to an external site., The University of Chicago Press, 2015.   
— a marine biologist turned film-maker tries to help scientists up their game for story telling
Hilary Glasman-Deal, Science Research Writing, for Native and Non-Native Speakers of EnglishLinks to an external site., 2nd Ed. (2021)  Online single-user @ SFU library.
— very empirical approach.  Has good advice on deconstructing a paper and some useful lists of words to use in standard occasions.
General Writing Resources
The Chicago Manual of Style.  The definitive (US) guide to English grammar and style.  SFU has online access.
Peck's English PointersLinks to an external site., includes information and quizzes on grammar, punctuation, usage and clarity
— your tax dollars at work:  An official Government of Canada site on grammar, style, usage, etc.
William Strunk and E. B. White, The Elements of StyleLinks to an external site..  The first editionLinks to an external site. (from 1919, without White's add-ons) is in the public domain.
— Old and somewhat dated, but still the book that defines discussions on style, whether you agree with it or not.
Empirical grammar.  Here is a modern tool, Google's Ngram viewerLinks to an external site..  Google has digitized essentially all English-language books, including technical ones and made it possible to search for words or short phrases.  It returns a graph of the empirical frequency of use. 

Application:  Use Ngrams to find which spelling is more commonly used.  Should you write "nonlinear" or "non-linear"? 
                       Enter them into the Ngram viewer to find out!
 