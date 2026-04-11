<div align="center">
  <h1><b>SparxFast</b></h1>
  <p><i>A quick and easy Sparx Maths question solver, built in Python, powered by Gemini API.</i></p>
</div>

## Features
- Always On-Top | This makes the SparxFast window above any other window on your desktop. Perfect for when it keeps hiding when you click on the browser window.
- Gemini | SparxFast is powered by Gemini 3.1 Flash. This Google's fastest model, more models coming soon.
- Bookwork Code Searcher | Get a Bookwork check, but didn't write it down on some paper or a text document? No need to worry, we log the AI's output in a log file, so you can click a button, enter the bookwork code, and you can see the answer.
- Automatic Update Detection | Found a bug, but you forgot you were on an older version on another piece of software? Don't worry, SparxFast has it's own built in updater, so you don't need to worry. (Issues have been detected, and updates may not always get detected.)

## Notes
- While Gemini is thinking, the app may freeze, or say (Not Responding) in the title bar. Please ignore this, it just means the Python script running in the background is waiting for Gemini to answer. <br>
- Administrator Access is required as the app stores it's data in the (root)\ProgramFiles directory. This directory cannot be edited without elevation. To fix this, we're going to let you customize the data directory, and make the SparxFast folder permissions into a standard user. This means UAC Prompts for SparxFast will not be needed, unless it's in a location where you need Administrator to edit or create files there.

## Installation

Option 1: Manual: Download from [Releases](https://github.com/frubby21/SparxFast/releases/latest) and run the executable. <br>
Option 2: WinGet (not updated as frequently (v1.0.4)): <br>
```bash
winget install com.frubby21.python.windows.sparxfast
```
