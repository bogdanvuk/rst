/*
 * generated by Xtext
 */
package rs.demsys.rst.ui;

import org.eclipse.ui.plugin.AbstractUIPlugin;
import org.eclipse.xtext.documentation.IEObjectDocumentationProvider;
import org.eclipse.xtext.ui.editor.hover.IEObjectHoverProvider;

import rs.demsys.rst.ui.hover.BibEObjectDocumentationProvider;
import rs.demsys.rst.ui.hover.BibEObjectHoverProvider;

/**
 * Use this class to register components to be used within the IDE.
 */
public class BibUiModule extends rs.demsys.rst.ui.AbstractBibUiModule {
	public BibUiModule(AbstractUIPlugin plugin) {
		super(plugin);
	}
	
	public Class<? extends IEObjectHoverProvider> bindIEObjectHoverProvider() {
        return BibEObjectHoverProvider.class;
    }
 
    public Class<? extends IEObjectDocumentationProvider> bindIEObjectDocumentationProviderr() {
        return BibEObjectDocumentationProvider.class;
    }
}
