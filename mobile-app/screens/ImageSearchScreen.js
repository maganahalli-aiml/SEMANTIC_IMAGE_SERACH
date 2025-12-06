import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Alert,
  Image,
  TouchableOpacity,
} from 'react-native';
import {
  Button,
  Card,
  Title,
  Paragraph,
  ActivityIndicator,
  Surface,
  Chip,
} from 'react-native-paper';
import * as ImagePicker from 'expo-image-picker';
import { searchByImage, getCategories } from '../services/api';
import SearchResults from '../components/SearchResults';

export default function ImageSearchScreen() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categories, setCategories] = useState([]);
  const [showCategories, setShowCategories] = useState(false);

  const pickImage = async (useCamera = false) => {
    // Request permissions
    if (useCamera) {
      const { status } = await ImagePicker.requestCameraPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Denied', 'Camera permission is required to take photos');
        return;
      }
    } else {
      const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Denied', 'Photo library permission is required');
        return;
      }
    }

    // Launch picker
    const result = useCamera
      ? await ImagePicker.launchCameraAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        })
      : await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        });

    if (!result.canceled && result.assets[0]) {
      setSelectedImage(result.assets[0].uri);
      setResults(null); // Clear previous results
    }
  };

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
    if (!selectedImage) {
      Alert.alert('Error', 'Please select an image first');
      return;
    }

    setLoading(true);
    try {
      const metadataFilter = selectedCategory ? { category: selectedCategory } : null;
      const data = await searchByImage(selectedImage, 10, metadataFilter, false);
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
    <ScrollView style={styles.container}>
      <Surface style={styles.surface} elevation={2}>
        <Title style={styles.title}>📷 Image Search</Title>
        <Paragraph style={styles.subtitle}>
          Find similar images using an image
        </Paragraph>

        <View style={styles.buttonContainer}>
          <Button
            mode="contained"
            onPress={() => pickImage(false)}
            style={styles.button}
            icon="image"
          >
            Choose Photo
          </Button>
          <Button
            mode="contained"
            onPress={() => pickImage(true)}
            style={styles.button}
            icon="camera"
          >
            Take Photo
          </Button>
        </View>

        {selectedImage && (
          <Card style={styles.imageCard}>
            <Card.Content>
              <Paragraph style={styles.imageLabel}>Selected Image:</Paragraph>
              <TouchableOpacity onPress={() => setSelectedImage(null)}>
                <Image source={{ uri: selectedImage }} style={styles.image} />
              </TouchableOpacity>
              <Paragraph style={styles.tapHint}>Tap to remove</Paragraph>
            </Card.Content>
          </Card>
        )}

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
          disabled={loading || !selectedImage}
          style={styles.searchButton}
          icon="magnify"
        >
          Search Similar Images
        </Button>
      </Surface>

      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" />
          <Paragraph style={styles.loadingText}>Searching...</Paragraph>
        </View>
      )}

      {results && !loading && (
        <SearchResults results={results} queryType="image" />
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
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
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  button: {
    flex: 1,
    marginHorizontal: 4,
  },
  imageCard: {
    marginBottom: 16,
  },
  imageLabel: {
    fontWeight: 'bold',
    marginBottom: 8,
  },
  image: {
    width: '100%',
    height: 250,
    borderRadius: 8,
    resizeMode: 'cover',
  },
  tapHint: {
    textAlign: 'center',
    color: '#666',
    fontSize: 12,
    marginTop: 8,
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
