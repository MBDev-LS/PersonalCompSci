
import colorist

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

colorist.bright_blue(strike(f'Hello there, you are a toad? Well that is COOOOOLLLLLL 1234.___'))

print(strike(f'Hello there, {colorist.BrightColor.BLUE}you are a toad{colorist.BrightColor.OFF}? Well that is COOOOOLLLLLL 1234.___'))
