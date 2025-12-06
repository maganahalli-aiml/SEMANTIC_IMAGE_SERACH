import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import {
  TextInput,
  Button,
  Card,
  Title,
  Paragraph,
  Chip,
  ActivityIndicator,
  Surface,
} from 'react-native-paper';
import { searchByText, getCategories } from '../services/api';
import SearchResults from '../components/SearchResults';

export default function TextSearchScreen() {
  const [queryText, setQueryText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categories, setCategories] = useState([]);
  const [showCategories, setShowCategories] = useState(false);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data.categories || []);
      setShowCategories(true);
    } catch (error) {
      Alert.alert('Error', 'Failed to load categories');
    }
  };

  const handleSearch = async () => {
    if (!queryText.trim()) {
      Alert.alert('Error', 'Please enter a search query');
      return;
    }

    setLoading(true);
    try {
      const metadataFilter = selectedCategory ? { category: selectedCategory } : null;
      const data = await searchByText(queryText, 10, metadataFilter, false);
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
      Alert.alert(
        'Search Failed',
        error.response?.data?.detail?.message || error.message || 'An error occurred'
      );
    } finally {
      setLoading(false);
    }
  };

  const clearFilter = () => {
    setSelectedCategory(null);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView style={styles.scrollView}>
        <Surface style={styles.surface} elevation={2}>
          <Title style={styles.title}>🔍 Text Search</Title>
          <Paragraph style={styles.subtitle}>
            Search for images using natural language
          </Paragraph>

          <TextInput
            mode="outlined"
            label="Search Query"
            placeholder="e.g., yellow flowers, wild animals, sunset..."
            value={queryText}
            onChangeText={setQueryText}
            style={styles.input}
            multiline
          />

          <View style={styles.filterSection}>
            <Button
              mode="outlined"
              onPress={loadCategories}
              style={styles.filterButton}
              icon="filter"
            >
              {selectedCategory ? 'Change Filter' : 'Add Filter'}
            </Button>

            {selectedCategory && (
              <Chip
                selected
                onClose={clearFilter}
                style={styles.selectedChip}
              >
                {selectedCategory}
              </Chip>
            )}
          </View>

          {showCategories && (
            <Card style={styles.categoryCard}>
              <Card.Content>
                <Title style={styles.categoryTitle}>Filter by Category</Title>
                <View style={styles.chipContainer}>
                  {categories.map((category) => (
                    <Chip
                      key={category}
                      selected={selectedCategory === category}
                      onPress={() => {
                        setSelectedCategory(category);
                        setShowCategories(false);
                      }}
                      style={styles.chip}
                    >
                      {category}
                    </Chip>
                  ))}
                </View>
                <Button
                  mode="text"
                  onPress={() => setShowCategories(false)}
                  style={styles.closeButton}
                >
                  Close
                </Button>
              </Card.Content>
            </Card>
          )}

          <Button
            mode="contained"
            onPress={handleSearch}
            loading={loading}
            disabled={loading || !queryText.trim()}
            style={styles.searchButton}
            icon="magnify"
          >
            Search
          </Button>
        </Surface>

        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" />
            <Paragraph style={styles.loadingText}>Searching...</Paragraph>
          </View>
        )}

        {results && !loading && (
          <SearchResults results={results} queryType="text" />
        )}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
  },
  surface: {
    margin: 16,
    padding: 16,
    borderRadius: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    color: '#666',
    marginBottom: 16,
  },
  input: {
    marginBottom: 16,
  },
  filterSection: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    flexWrap: 'wrap',
  },
  filterButton: {
    marginRight: 8,
  },
  selectedChip: {
    marginRight: 8,
  },
  categoryCard: {
    marginBottom: 16,
  },
  categoryTitle: {
    fontSize: 16,
    marginBottom: 12,
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 8,
  },
  chip: {
    margin: 4,
  },
  closeButton: {
    marginTop: 8,
  },
  searchButton: {
    paddingVertical: 6,
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 32,
  },
  loadingText: {
    marginTop: 16,
    color: '#666',
  },
});
