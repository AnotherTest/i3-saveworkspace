== Save i3 workspaces ==

This very hacky and incomplete script saves your i3 workspaces to a file.
Later, it is possible to load that file and build up the workspace.

=== Dependencies ===

* Tested and written with Python 2.7. Python 3 might (not) work.
* The i3 window manager.
* The py-i3 library.
* The xdotool (apt-get install xdotool for debian).

=== Todo ===

* Doesn't handle tabbed and stacked mode yet.
* Use command-line options instead of prompting for input.
* Cleanup the hacky code.
* There's probably a better way to focus the right windows than using 
  the mouse.
* Find and fix bugs!
