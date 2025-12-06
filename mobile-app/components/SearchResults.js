import React from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Card, Title, Paragraph, Chip, Divider } from 'react-native-paper';

export default function SearchResults({ results, queryType }) {
  if (!results || !results.results || results.results.length === 0) {
    return (
      <Card style={styles.emptyCard}>
        <Card.Content>
          <Title>No Results</Title>
          <Paragraph>No images found matching your search.</Paragraph>
        </Card.Content>
      </Card>
    );
  }

  const renderResult = ({ item, index }) => (
    <Card style={styles.resultCard} key={item.id}>
      <Card.Content>
        <View style={styles.header}>
          <Chip style={styles.rankChip}>#{index + 1}</Chip>
          <Chip style={styles.scoreChip}>
            Score: {(item.score * 100).toFixed(1)}%
          </Chip>
        </View>

        <Divider style={styles.divider} />

        {item.payload && (
          <View style={styles.metadata}>
            {item.payload.filename && (
              <View style={styles.metadataRow}>
                <Paragraph style={styles.label}>Filename:</Paragraph>
                <Paragraph style={styles.value}>{item.payload.filename}</Paragraph>
              </View>
            )}

            {item.payload.category && (
              <View style={styles.metadataRow}>
                <Paragraph style={styles.label}>Category:</Paragraph>
                <Chip mode="outlined" style={styles.categoryChip}>
                  {item.payload.category}
                </Chip>
              </View>
            )}

            {item.payload.path && (
              <View style={styles.metadataRow}>
                <Paragraph style={styles.label}>Path:</Paragraph>
                <Paragraph style={styles.pathValue} numberOfLines={2}>
                  {item.payload.path}
                </Paragraph>
              </View>
            )}
          </View>
        )}
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      <Card style={styles.summaryCard}>
        <Card.Content>
          <Title>Search Results</Title>
          <Paragraph style={styles.summary}>
            Found {results.total_results} image{results.total_results !== 1 ? 's' : ''} 
            {' '}(Query ID: {results.query_id.substring(0, 8)}...)
          </Paragraph>
          <Chip icon="magnify" style={styles.typeChip}>
            {queryType === 'text' ? 'Text Search' : 'Image Search'}
          </Chip>
        </Card.Content>
      </Card>

      <FlatList
        data={results.results}
        renderItem={renderResult}
        keyExtractor={(item) => item.id}
        scrollEnabled={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    paddingTop: 0,
  },
  summaryCard: {
    marginBottom: 16,
  },
  summary: {
    color: '#666',
    marginTop: 4,
    marginBottom: 8,
  },
  typeChip: {
    alignSelf: 'flex-start',
  },
  emptyCard: {
    margin: 16,
  },
  resultCard: {
    marginBottom: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  rankChip: {
    backgroundColor: '#e3f2fd',
  },
  scoreChip: {
    backgroundColor: '#e8f5e9',
  },
  divider: {
    marginBottom: 12,
  },
  metadata: {
    gap: 8,
  },
  metadataRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
  },
  label: {
    fontWeight: 'bold',
    marginRight: 8,
    color: '#555',
  },
  value: {
    flex: 1,
    color: '#333',
  },
  pathValue: {
    flex: 1,
    color: '#666',
    fontSize: 12,
  },
  categoryChip: {
    height: 28,
  },
});
