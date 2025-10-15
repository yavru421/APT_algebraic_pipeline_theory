# APT-OpenSCAD README

This folder contains the Algebraic Pipeline Theory (APT) CLI application for chatting with Llama-3.3-70B-Instruct and updating an OpenSCAD view in real time.

## Structure
- `cli_llama_scad_chat.py`: Main CLI pipeline script
- `tests/`: Unit tests for pipeline modules

## Usage
1. Install Python dependencies: `pip install -r ../requirements.txt`
2. Install OpenSCAD from https://openscad.org/ (for view updates)
3. Run: `python cli_llama_scad_chat.py --model Llama-3.3-70B-Instruct`

## Pipeline Equation
    y_final = m6(m5(m4(m3(m2(m1(x1), x4), x3)), x2))

## Test
Run tests from this directory:
    pytest tests/

## Notes
- The CLI will update the OpenSCAD view if the Llama response contains SCAD code.
- All steps are modular and follow APT algebraic pipeline methodology.
