package rs.demsys.rst.ui.hyperlink;

import java.util.List;

import org.eclipse.ui.IEditorDescriptor;
import org.eclipse.ui.IWorkbenchPage;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PartInitException;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.ide.IDE;
import org.eclipse.xtext.ui.editor.hyperlinking.HyperlinkHelper;
import org.eclipse.core.resources.IFile;
import org.eclipse.core.resources.IResource;
import org.eclipse.core.resources.IWorkspaceRoot;
import org.eclipse.core.resources.ResourcesPlugin;
import org.eclipse.core.runtime.Path;
import org.eclipse.core.runtime.URIUtil;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.URIConverter;
import org.eclipse.jface.text.Region;
import org.eclipse.xtext.RuleCall;
import org.eclipse.xtext.nodemodel.INode;
import org.eclipse.xtext.nodemodel.impl.AbstractNode;
import org.eclipse.xtext.nodemodel.util.NodeModelUtils;
import org.eclipse.xtext.resource.EObjectAtOffsetHelper;
import org.eclipse.xtext.resource.XtextResource;
import org.eclipse.xtext.resource.impl.ResourceDescriptionsProvider;
import org.eclipse.xtext.scoping.IGlobalScopeProvider;
import org.eclipse.xtext.scoping.impl.ImportUriGlobalScopeProvider;
import org.eclipse.xtext.scoping.impl.ImportUriResolver;
import org.eclipse.xtext.ui.editor.hyperlinking.HyperlinkHelper;
import org.eclipse.xtext.ui.editor.hyperlinking.IHyperlinkAcceptor;
import org.eclipse.xtext.ui.editor.hyperlinking.IHyperlinkHelper;
import org.eclipse.xtext.ui.editor.hyperlinking.XtextHyperlink;
import org.eclipse.xtext.util.PolymorphicDispatcher;

import com.google.common.collect.Lists;
import com.google.inject.Inject;
import com.google.inject.Provider;

import rs.demsys.rst.rst.*;
import rs.demsys.rst.services.RstGrammarAccess;

public class RstHyperlinkHelper extends HyperlinkHelper {
	@Inject
    RstGrammarAccess ga;
    
    @Inject
    ImportUriResolver r;
    
    @Inject
    private Provider<XtextHyperlink> hyperlinkProvider;
    
    @Inject
    private Provider<RstGeneralHyperlink> rstGenHyperlinkProvider;
    
    @Inject
    ImportUriGlobalScopeProvider gsp;
    
    @Inject private EObjectAtOffsetHelper eObjectAtOffsetHelper;
    
    private PolymorphicDispatcher<Void> createHypelinkFor = PolymorphicDispatcher.createForSingleTarget("createHyperlink", 3, 3, this);
    
    public void createHyperlink(EObject obj, XtextResource resource, IHyperlinkAcceptor acceptor)
    {
    }
    
    public RstGeneralHyperlink createGeneralHyperlink(String text, IFile file, int offset, int length)
    {
    	RstGeneralHyperlink result = rstGenHyperlinkProvider.get();
        //result.setURI(URI.createURI(file.getLocation().toString()));
    	result.setURI(URI.createURI(file.getLocationURI().toString()));
        Region region = new Region(offset, length);
        result.setHyperlinkRegion(region);
        result.setHyperlinkText(text);
        result.setFile(file);
        
        return result;
    }
    
    public XtextHyperlink createXtextHyperlink(String text, IFile file, int offset, int length)
    {
    	XtextHyperlink result = hyperlinkProvider.get();
        result.setURI(URI.createURI(file.getLocationURI().toString()));
    	//result.setURI(file.getLocationURI());
        Region region = new Region(offset, length);
        result.setHyperlinkRegion(region);
        result.setHyperlinkText(text);
        
        return result;
    }
    
    public IFile findFileFromRelativePath(XtextResource resource, String relFileName)
    {
    	String platformString = resource.getURI().toPlatformString(true);
		IFile curFile = ResourcesPlugin.getWorkspace().getRoot().getFile(new Path(platformString));

		URI uri = URI.createURI(relFileName);
    	URI resFile = URI.createURI(curFile.getProjectRelativePath().toString());
    	uri = resFile.trimSegments(1).appendSegments(uri.segments());
        

        
		
		
		//IFile file = curFile.getProject().getFile(new Path(uriFile.toString()));
    	IFile file = curFile.getProject().getFile(new Path(uri.toString()));
		return file;
    }
    
    public void createHyperlink(BibDirective obj, XtextResource resource, IHyperlinkAcceptor acceptor) {
    	List<INode> nodes = NodeModelUtils.findNodesForFeature(obj,
				 RstPackage.eINSTANCE.getBibDirective_Bib());
	    if (!nodes.isEmpty()) 
	    {
			IFile file = findFileFromRelativePath(resource, obj.getBib());
			
			if (file.isAccessible()) {
			    acceptor.accept(createGeneralHyperlink(obj.getBib(), file, nodes.get(0).getOffset(), nodes.get(0).getLength()));
			}
	    }
    }
    
    public void createHyperlink(ImageDirective obj, XtextResource resource, IHyperlinkAcceptor acceptor) {
    	List<INode> nodes = NodeModelUtils.findNodesForFeature(obj,
				 RstPackage.eINSTANCE.getImageDirective_Picture());
	    if (!nodes.isEmpty()) {
	    	INode node = nodes.get(0);
	        
	    	String uriString = obj.getPicture();
	        
			IFile file = findFileFromRelativePath(resource, uriString);
			
			if (file.isAccessible()) {
			    acceptor.accept(createGeneralHyperlink(uriString, file, node.getOffset(), node.getLength()));
			}
	    }
    }
    
    public void createHyperlink(IncludeDirective obj, XtextResource resource, IHyperlinkAcceptor acceptor) {
    	List<INode> nodes = NodeModelUtils.findNodesForFeature(obj,
				 RstPackage.eINSTANCE.getIncludeDirective_ImportURI());
	    if (!nodes.isEmpty()) {
	    	INode node = nodes.get(0);
	        String uriString = ((IncludeDirective) obj).getImportURI();
	         
	        URI uri = URI.createURI(uriString);
//            final URIConverter uriConverter = resource.getResourceSet().getURIConverter();
//            final URI normalized = uri.isPlatformResource() ? uri : uriConverter.normalize(uri);
           
            IFile file = findFileFromRelativePath(resource, uriString);
			
			if (file.isAccessible()) {
			    acceptor.accept(createXtextHyperlink(uriString, file, node.getOffset(), node.getLength()));
			}
           
//           if (gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)) != null)
//           {
//               final URI targetURI = gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)).getResourceDescription(normalized).getURI();
//               XtextHyperlink result = hyperlinkProvider.get();
//               result.setURI(targetURI);
//               Region region = new Region(node.getOffset(), node.getLength());
//               result.setHyperlinkRegion(region);
//               result.setHyperlinkText(uriString);
//               acceptor.accept(result);
//           } 
	    }
    }
    
    @Override
    public void createHyperlinksByOffset(XtextResource resource, int offset,
                    IHyperlinkAcceptor acceptor) {

    	EObject eObject = eObjectAtOffsetHelper.resolveElementAt(resource, offset);
    	
    	if (eObject != null)
    	{
    		createHypelinkFor.invoke(eObject, resource, acceptor);
    	}
    	
//    	if (eObject instanceof IncludeDirective) {
//    		
//    	}
    	super.createHyperlinksByOffset(resource, offset, acceptor);
    }
}
    	
//        INode node = NodeModelUtils.findLeafNodeAtOffset(resource.getParseResult().getRootNode(), offset);
//        
//        if (node != null && node.getSemanticElement() instanceof IncludeDirective) {
//        	if (node.getGrammarElement() instanceof RuleCall)
//        	{
//        		IncludeDirective obj = (IncludeDirective) NodeModelUtils.findActualSemanticObjectFor(node);
//    	        INode semanticNode = NodeModelUtils.findActualNodeFor(obj);
//    	        
//                String uriString = obj.getImportURI(); //i.getImportURI().toString();
//                URI uri = URI.createURI(uriString);
//                final URIConverter uriConverter = resource.getResourceSet().getURIConverter();
//                final URI normalized = uri.isPlatformResource() ? uri : uriConverter.normalize(uri);
//                
//                if (gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)) != null)
//                {
//                	
//	                final URI targetURI = gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)).getResourceDescription(normalized).getURI();
//	                XtextHyperlink result = hyperlinkProvider.get();
//	                result.setURI(targetURI);
//	                Region region = new Region(semanticNode.getOffset(), semanticNode.getLength());
//	                result.setHyperlinkRegion(region);
//	                result.setHyperlinkText(uriString);
//	                acceptor.accept(result);
//                }            
//        	}
//        }
        
//        if (node != null && node.getSemanticElement() instanceof FileName) {
//            
//	        EObject obj = NodeModelUtils.findActualSemanticObjectFor(node);
//	        INode semanticNode = NodeModelUtils.findActualNodeFor(obj);            
//        //if (node != null && node.getSemanticElement() instanceof IncludeDirective) {
//            //if (ga.getFileNameRule().equals(((RuleCall)node.getGrammarElement()).getRule())) {
////                IncludeDirective i = (IncludeDirective) semanticNode.getParent().getSemanticElement();
//                String uriString = semanticNode.getText(); //i.getImportURI().toString();
////                String uriString = i.getImportURI().toString();
//                URI uri = URI.createURI(uriString);
//                final URIConverter uriConverter = resource.getResourceSet().getURIConverter();
//                final URI normalized = uri.isPlatformResource() ? uri : uriConverter.normalize(uri);
//                
//                if (gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)) != null)
//                {
//                	
//	                final URI targetURI = gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)).getResourceDescription(normalized).getURI();
//	//                XtextHyperlink result = hyperlinkProvider.get();
//	//                final URI targetURI = gsp.resourceDescriptionsProvider.getResourceDescriptions(resource).getURI();
//	                XtextHyperlink result = hyperlinkProvider.get();
//	                result.setURI(targetURI);
//	                Region region = new Region(semanticNode.getOffset(), semanticNode.getLength());
//	                result.setHyperlinkRegion(region);
//	                result.setHyperlinkText(uriString);
//	//                System.out.println(uriString);
//	                //result.open();
//	                acceptor.accept(result);
//                }            
//        }
//        super.createHyperlinksByOffset(resource, offset, acceptor);
//    }
// }
