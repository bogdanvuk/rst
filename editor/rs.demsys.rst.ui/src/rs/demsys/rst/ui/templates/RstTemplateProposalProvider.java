package rs.demsys.rst.ui.templates;

import org.eclipse.jface.text.templates.ContextTypeRegistry;
import org.eclipse.jface.text.templates.Template;
import org.eclipse.jface.text.templates.TemplateContext;
import org.eclipse.jface.text.templates.TemplateProposal;
import org.eclipse.jface.text.templates.persistence.TemplateStore;
import org.eclipse.xtext.ui.editor.contentassist.ContentAssistContext;
import org.eclipse.xtext.ui.editor.contentassist.ITemplateAcceptor;
import org.eclipse.xtext.ui.editor.templates.ContextTypeIdHelper;
import org.eclipse.xtext.ui.editor.templates.DefaultTemplateProposalProvider;

import rs.demsys.rst.services.RstGrammarAccess;

import com.google.inject.Inject;

public class RstTemplateProposalProvider extends
		DefaultTemplateProposalProvider {

	ContextTypeIdHelper helper;
	
	@Inject
	public RstTemplateProposalProvider(TemplateStore templateStore,
			ContextTypeRegistry registry, ContextTypeIdHelper helper) {
		super(templateStore, registry, helper);
		this.helper=helper;
	}

	@Inject
	RstGrammarAccess ga;
	
	@Override
	protected void createTemplates(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		// "regular templates"
		super.createTemplates(templateContext, context, acceptor);

		// add your own
		
		String id=helper.getId(ga.getSectionRule());
		
		if(templateContext.getContextType().getId().equals(id)){
			// create a template on the fly
			Template template = new Template(
					"fig - Insert new figure",
					"Inserts new figure into the document.",
					"uniqueTemplateID",
					".. _fig-${label}:\n" +
					"\n" +
					".. figure:: ${file_name}\n" +
					"    \n" +
					"    ${caption}\n",
					true);// auto-insertable?
	
			// create a proposal
			TemplateProposal tp = createProposal(template, templateContext,
					context, getImage(template), getRelevance(template));
	
			// make it available
			acceptor.accept(tp);
		}
	}

}
