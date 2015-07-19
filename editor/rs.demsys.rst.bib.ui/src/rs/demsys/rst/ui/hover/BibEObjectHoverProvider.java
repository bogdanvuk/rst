package rs.demsys.rst.ui.hover;

import org.eclipse.emf.ecore.EObject;
import org.eclipse.jface.text.IRegion;
import org.eclipse.jface.text.ITextViewer;
import org.eclipse.xtext.ui.editor.hover.html.DefaultEObjectHoverProvider;
import org.eclipse.xtext.util.PolymorphicDispatcher;

public class BibEObjectHoverProvider extends DefaultEObjectHoverProvider{

	private PolymorphicDispatcher<String> getFirstLineDispatch = PolymorphicDispatcher.createForSingleTarget("getFirstLineFor", 1, 1, this);
	
	@Override
	protected String getFirstLine(EObject o) {
		if (o != null)
    	{
			return getFirstLineDispatch.invoke(o);
    	}
		return "";
	}
		
	public String getFirstLineFor(EObject obj) {
		return super.getFirstLine(obj);
	}
	
}
