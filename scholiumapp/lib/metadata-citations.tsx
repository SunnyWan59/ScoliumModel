import { generateAPACitation, generateMLACitation, generateChicagoCitation, generateHarvardCitation, generateVancouverCitation, CitationData, Author } from "./citation-styles";


/**
 * Converts raw metadata into structured CitationData format
 * @param rawMetadata Raw metadata object from source
 * @returns Formatted CitationData object
 */
function formatMetadata(rawMetadataList: any[]): CitationData[] {
  return rawMetadataList.map(rawMetadata => {
    // Extract and format authors
    const authors: Author[] = [];
    if (rawMetadata.authors) {
      // Parse author string into individual authors
      const authorString = rawMetadata.authors;
      
      // Handle different formats of author strings
      if (typeof authorString === 'string') {
        // Split by semicolons for format like "Vaswani, Ashish; Shankar, Noam; ..."
        const authorList = authorString.split(';').map(author => author.trim());
        
        authorList.forEach(author => {
          if (author) {
            // Handle "et al." case
            if (author.toLowerCase().includes('et al')) {
              // Skip "et al." as it's not a specific author
              return;
            }
            
            // Parse "LastName, FirstName" format
            const parts = author.split(',').map(part => part.trim());
            if (parts.length >= 2) {
              authors.push({
                lastName: parts[0],
                firstName: parts[1]
              });
            } else {
              // Handle cases where there's no comma (just use as lastName)
              authors.push({
                lastName: author,
                firstName: ''
              });
            }
          }
        });
      } else if (Array.isArray(authorString)) {
        // Handle case where authors might already be an array
        authorString.forEach(author => {
          if (typeof author === 'string') {
            const parts = author.split(',').map(part => part.trim());
            if (parts.length >= 2) {
              authors.push({
                lastName: parts[0],
                firstName: parts[1]
              });
            } else {
              authors.push({
                lastName: author,
                firstName: ''
              });
            }
          } else if (typeof author === 'object' && author !== null) {
            // Handle case where author might be an object with name properties
            authors.push({
              lastName: author.lastName || author.last_name || '',
              firstName: author.firstName || author.first_name || ''
            });
          }
        });
      }
    }

    // Extract other citation fields with fallbacks
    return {
      authors,
      title: rawMetadata.title || '',
      publisher: rawMetadata.publisher || 'arXiv',
      year: rawMetadata.year?.toString() || ''
    };
  });
}


/**
 * Generates citations from metadata based on the specified citation style
 * @param metadata Array of citation metadata
 * @param style Citation style (APA, MLA, Chicago, Harvard, or Vancouver)
 * @returns Array of formatted citations
 */
function generateCitations(metadata: CitationData[], style: string): string[] {
  return metadata.map(data => {
    switch(style.toUpperCase()) {
      case "APA":
        return generateAPACitation(data);
      case "MLA": 
        return generateMLACitation(data);
      case "CHICAGO":
        return generateChicagoCitation(data);
      case "HARVARD":
        return generateHarvardCitation(data);
      case "VANCOUVER":
        return generateVancouverCitation(data);
      default:
        return generateAPACitation(data); // Default to APA if style not recognized
    }
  });
}

/**
 * Combines metadata extraction and citation generation into a single function
 * @param rawMetadata Array of raw metadata objects
 * @param style Citation style (APA, MLA, Chicago, Harvard, or Vancouver)
 * @returns Array of formatted citations
 */
export function processAndGenerateCitations(rawMetadata: any[], style: string): string[] {
  // First convert raw metadata into CitationData format
  const citationData = formatMetadata(rawMetadata);
  
  // Then generate citations in requested style
  return generateCitations(citationData, style);
}


