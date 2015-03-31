package rs.demsys.rst.plugin.projects;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;

import org.eclipse.core.internal.events.BuildCommand;
import org.eclipse.core.resources.IBuildConfiguration;
import org.eclipse.core.resources.ICommand;
import org.eclipse.core.resources.IContainer;
import org.eclipse.core.resources.IFolder;
import org.eclipse.core.resources.IProject;
import org.eclipse.core.resources.IProjectDescription;
import org.eclipse.core.resources.IResource;
import org.eclipse.core.resources.ResourcesPlugin;
import org.eclipse.core.runtime.Assert;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IProgressMonitor;

import rs.demsys.rst.plugin.RstProjectBuilder;
import rs.demsys.rst.plugin.natures.ProjectNature;

public class CustomProjectSupport {
	/**
     * For this marvelous project we need to:
     * - create the default Eclipse project
     * - add the custom project nature
     * - create the folder structure
     *
     * @param projectName
     * @param location
     * @param natureId
     * @return
     */
    public static IProject createProject(String projectName, String authorName, String version, URI location) {
        Assert.isNotNull(projectName);
        Assert.isTrue(projectName.trim().length() > 0);
 
        IProject project = createBaseProject(projectName, location);
        try {
            addNature(project);
            addBuilder(project);
            
            String[] cmd = new String[10];
            String s = null;
            
            cmd[0] = "sphinx-quickstart";
            cmd[1] = project.getLocation().toString();
            cmd[2] = "-q";
            cmd[3] = "--sep";
            cmd[4] = "-p";
            cmd[5] = projectName;
            cmd[6] = "-a";
            cmd[7] = authorName;
            cmd[8] = "-v";
            cmd[9] = version;

            Process p = Runtime.getRuntime().exec(cmd);
            
            while(p.isAlive())
            {}
            
//            BufferedReader stdInput = new BufferedReader(new
//                    InputStreamReader(p.getInputStream()));
//    
//           BufferedReader stdError = new BufferedReader(new
//                InputStreamReader(p.getErrorStream()));
//
//           // read the output from the command
//           System.out.println("Here is the standard output of the command:\n");
//           while ((s = stdInput.readLine()) != null) {
//               System.out.println(s);
//           }
//            
//           // read any errors from the attempted command
//           System.out.println("Here is the standard error of the command (if any):\n");
//           while ((s = stdError.readLine()) != null) {
//               System.out.println(s);
//           }
            
            project.refreshLocal(IResource.DEPTH_INFINITE, null);
            
            //String[] paths = { "parent/child1-1/child2", "parent/child1-2/child2/child3" }; //$NON-NLS-1$ //$NON-NLS-2$
            //addToProjectStructure(project, paths);
        } catch (CoreException e) {
            e.printStackTrace();
            project = null;
        } catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
 
        return project;
    }
 
    /**
     * Just do the basics: create a basic project.
     *
     * @param location
     * @param projectName
     */
    private static IProject createBaseProject(String projectName, URI location) {
        // it is acceptable to use the ResourcesPlugin class
        IProject newProject = ResourcesPlugin.getWorkspace().getRoot().getProject(projectName);
 
        if (!newProject.exists()) {
            URI projectLocation = location;
            IProjectDescription desc = newProject.getWorkspace().newProjectDescription(newProject.getName());
            if (location != null && ResourcesPlugin.getWorkspace().getRoot().getLocationURI().equals(location)) {
                projectLocation = null;
            }
 
            desc.setLocationURI(projectLocation);
            try {
                newProject.create(desc, null);
                if (!newProject.isOpen()) {
                    newProject.open(null);
                }
            } catch (CoreException e) {
                e.printStackTrace();
            }
        }
 
        return newProject;
    }
 
    private static void createFolder(IFolder folder) throws CoreException {
        IContainer parent = folder.getParent();
        if (parent instanceof IFolder) {
            createFolder((IFolder) parent);
        }
        if (!folder.exists()) {
            folder.create(false, true, null);
        }
    }
 
    /**
     * Create a folder structure with a parent root, overlay, and a few child
     * folders.
     *
     * @param newProject
     * @param paths
     * @throws CoreException
     */
    private static void addToProjectStructure(IProject newProject, String[] paths) throws CoreException {
        for (String path : paths) {
            IFolder etcFolders = newProject.getFolder(path);
            createFolder(etcFolders);
        }
    }
 
    private static void addBuilder(IProject project) throws CoreException
    {
    	   IProjectDescription desc = project.getDescription();
    	   ICommand[] commands = desc.getBuildSpec();
    	   boolean found = false;

    	   for (int i = 0; i < commands.length; ++i) {
    	      if (commands[i].getBuilderName().equals(RstProjectBuilder.BUILDER_ID)) {
    	         found = true;
    	         break;
    	      }
    	   }
    	   if (!found) { 
    	      //add builder to project
    	      ICommand command = desc.newCommand();
    	      command.setBuilderName(RstProjectBuilder.BUILDER_ID);
    	      ICommand[] newCommands = new ICommand[commands.length + 1];

    	      // Add it before other builders.
    	      System.arraycopy(commands, 0, newCommands, 1, commands.length);
    	      newCommands[0] = command;
    	      desc.setBuildSpec(newCommands);
    	      project.setDescription(desc, null);
    	   }
    }
    
    private static void addNature(IProject project) throws CoreException {
        if (!project.hasNature(ProjectNature.NATURE_ID)) {
            IProjectDescription description = project.getDescription();
            String[] prevNatures = description.getNatureIds();
            String[] newNatures = new String[prevNatures.length + 2];
            System.arraycopy(prevNatures, 0, newNatures, 0, prevNatures.length);
            newNatures[prevNatures.length] = ProjectNature.NATURE_ID;
            newNatures[prevNatures.length+1] = "org.eclipse.xtext.ui.shared.xtextNature";
            description.setNatureIds(newNatures);
            
            IProgressMonitor monitor = null;
            project.setDescription(description, monitor);
        }
    }
}
