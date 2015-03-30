package rs.demsys.rst.plugin.wizards;

import java.net.URI;

import org.eclipse.jface.viewers.IStructuredSelection;
import org.eclipse.jface.wizard.Wizard;
import org.eclipse.ui.INewWizard;
import org.eclipse.ui.IWorkbench;
import org.eclipse.ui.dialogs.WizardNewProjectCreationPage;

import rs.demsys.rst.plugin.projects.CustomProjectSupport;

public class NewProjectWizard extends Wizard implements INewWizard {

	private RstNewProjectCreationPage _pageOne;
	
	public NewProjectWizard() {
		setWindowTitle("Rst Project");
	}

	@Override
	public void init(IWorkbench workbench, IStructuredSelection selection) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean performFinish() {
		String name = _pageOne.getProjectName();
	    URI location = null;
	    if (!_pageOne.useDefaults()) {
	        location = _pageOne.getLocationURI();
	    } // else location == null
	 
	    CustomProjectSupport.createProject(name, _pageOne.getAuthorName(), _pageOne.getVersion(), location);
	 
	    return true;
	}
	
	@Override
	public void addPages() {
	    super.addPages();
	 
	    _pageOne = new RstNewProjectCreationPage("New Rst Project Wizard");
	    _pageOne.setTitle("Rst Project");
	    _pageOne.setDescription("This will create new Rst project.");
	 
	    addPage(_pageOne);
	}

}
