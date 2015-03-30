package rs.demsys.rst.ui.hyperlink;

import org.eclipse.core.resources.IFile;
import org.eclipse.ui.IWorkbenchPage;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PartInitException;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.ide.IDE;
import org.eclipse.xtext.ui.editor.hyperlinking.XtextHyperlink;

public class RstGeneralHyperlink extends XtextHyperlink {
	IFile ffile;
	
	public void setFile(IFile file)
	{
		ffile = file;
	}
	
	
	@Override
	public void open() {
		IWorkbenchWindow window = PlatformUI.getWorkbench().getActiveWorkbenchWindow();
		IWorkbenchPage page = window.getActivePage();
	  
		try {
			IDE.openEditor(page, ffile, true);
		} catch (PartInitException e) {
			e.printStackTrace();
		}
	}
}
