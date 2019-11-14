

def main():
    filename='examples/new/uart_synth.rtl.v'
    with open(filename) as f:
        content = f.read().replace(' .gnd(gnd), .vdd(vdd),', '')
    
    with open(filename[:-2] + "_new.v", "w") as text_file:
        text_file.write(content)
    
    
    
    
    
if __name__=='__main__':
    main()