package rs.demsys.rst.plugin;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Map;

import org.eclipse.core.resources.IProject;
import org.eclipse.core.resources.IResourceDelta;
import org.eclipse.core.resources.IncrementalProjectBuilder;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.ui.console.ConsolePlugin;
import org.eclipse.ui.console.IConsole;
import org.eclipse.ui.console.IConsoleManager;
import org.eclipse.ui.console.MessageConsole;
import org.eclipse.ui.console.MessageConsoleStream;

public class RstProjectBuilder extends IncrementalProjectBuilder {

	public static final String BUILDER_ID = "rs.demsys.rst.plugin.rstProjectBuilder";
	
	public RstProjectBuilder() {
		// TODO Auto-generated constructor stub
	}

	private MessageConsole findConsole(String name) {
		ConsolePlugin plugin = ConsolePlugin.getDefault();
		IConsoleManager conMan = plugin.getConsoleManager();
		IConsole[] existing = conMan.getConsoles();
		for (int i = 0; i < existing.length; i++)
			if (name.equals(existing[i].getName()))
				return (MessageConsole) existing[i];
		// no console found, so create a new one
		MessageConsole myConsole = new MessageConsole(name, null);
		conMan.addConsoles(new IConsole[] { myConsole });
		return myConsole;
	}
	
	@Override
	protected IProject[] build(int kind, Map<String, String> args,
			IProgressMonitor monitor) throws CoreException {
		// TODO Auto-generated method stub

		// get the project to build
		IProject project = getProject();

        try {
        	
    		String[] cmd = new String[4];
    		String s = null;
    		
    		cmd[0] = "make";
            cmd[1] = "-f";
            cmd[2] = project.getLocation().toString() + "/Makefile";
            cmd[3] = "latexpdf";
            		
            MessageConsole console = findConsole("Rst Console");
            MessageConsoleStream consoleOut = console.newMessageStream();
            
			Process p = Runtime.getRuntime().exec(cmd, null, new File(project.getLocation().toString()));
			
			BufferedReader stdInput = new BufferedReader(new InputStreamReader(
					p.getInputStream()));

			BufferedReader stdError = new BufferedReader(new InputStreamReader(
					p.getErrorStream()));

//			while (p.isAlive())
//			{
				while ((s = stdInput.readLine()) != null) {
					System.out.println(s);
					consoleOut.println(s);
				}
				
				while ((s = stdError.readLine()) != null) {
					System.out.println(s);
					consoleOut.println(s);
				}
//			}
				
			p.destroy();

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		switch (kind) {

		case FULL_BUILD:
			//System.out.println("Full builder triggered");
			break;

		case INCREMENTAL_BUILD:
			//System.out.println("Incremental triggered");
			break;

		case AUTO_BUILD:
			//IResourceDelta delta = getDelta(getProject());
			//System.out.println("Auto builder triggered");
			break;
		}
		
		return null;
	}

}
