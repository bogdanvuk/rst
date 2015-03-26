package rs.demsys.rst.ui.hyperlink;

import java.util.List;

import org.eclipse.xtext.ui.editor.hyperlinking.HyperlinkHelper;
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

import com.google.common.collect.Lists;
import com.google.inject.Inject;
import com.google.inject.Provider;





//import rs.demsys.rst.rst.EString;
//import rs.demsys.rst.rst.FileName;
import rs.demsys.rst.rst.IncludeDirective;
import rs.demsys.rst.rst.RstPackage;
import rs.demsys.rst.services.RstGrammarAccess;

public class RstHyperlinkHelper extends HyperlinkHelper {
	@Inject
    RstGrammarAccess ga;
    
    @Inject
    ImportUriResolver r;
    
    @Inject
    private Provider<XtextHyperlink> hyperlinkProvider;
    
    @Inject
    ImportUriGlobalScopeProvider gsp;
    
    @Inject private EObjectAtOffsetHelper eObjectAtOffsetHelper;
    
    @Override
    public void createHyperlinksByOffset(XtextResource resource, int offset,
                    IHyperlinkAcceptor acceptor) {

    	EObject eObject = eObjectAtOffsetHelper.resolveElementAt(resource, offset);
    	
    	if (eObject instanceof IncludeDirective) {
    		List<INode> nodes = NodeModelUtils.findNodesForFeature(eObject,
    				 RstPackage.eINSTANCE.getIncludeDirective_ImportURI());
		    if (!nodes.isEmpty()) {
		    	INode node = nodes.get(0);
		        String uriString = ((IncludeDirective) eObject).getImportURI();
		         
		        URI uri = URI.createURI(uriString);
                final URIConverter uriConverter = resource.getResourceSet().getURIConverter();
                final URI normalized = uri.isPlatformResource() ? uri : uriConverter.normalize(uri);
                
                if (gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)) != null)
                {
	                final URI targetURI = gsp.getResourceDescriptions(resource, Lists.newArrayList(normalized)).getResourceDescription(normalized).getURI();
	                XtextHyperlink result = hyperlinkProvider.get();
	                result.setURI(targetURI);
	                Region region = new Region(node.getOffset(), node.getLength());
	                result.setHyperlinkRegion(region);
	                result.setHyperlinkText(uriString);
	                acceptor.accept(result);
                } 
		    }
    	}
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
