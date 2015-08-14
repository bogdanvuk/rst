package rs.demsys.rst.ui.hover;

import org.eclipse.core.internal.utils.FileUtil;
import org.eclipse.core.resources.IFile;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.jface.internal.text.html.HTMLPrinter;
import org.eclipse.xtext.documentation.IEObjectDocumentationProvider;
import org.eclipse.xtext.nodemodel.INode;
import org.eclipse.xtext.nodemodel.util.NodeModelUtils;
import org.eclipse.xtext.resource.XtextResource;
import org.eclipse.xtext.util.PolymorphicDispatcher;

import rs.demsys.rst.bib.Entry;

public class BibEObjectDocumentationProvider implements
		IEObjectDocumentationProvider {

	private PolymorphicDispatcher<String> getDocumentationDispatch = PolymorphicDispatcher.createForSingleTarget("getDocumentationFor", 1, 1, this);
	
	@Override
	public String getDocumentation(EObject o) {
		if (o != null)
    	{
			return getDocumentationDispatch.invoke(o);
    	}
		return "";
	}
	
	public String getDocumentationFor(EObject o) {
		return "";
	}
	
	public String getDocumentationFor(Entry obj) {
		return "<pre>" + NodeModelUtils.findActualNodeFor(obj).getText() + "</pre>";
	}

}
