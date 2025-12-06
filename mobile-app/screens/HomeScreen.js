import React, { useEffect, useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Alert,
  RefreshControl,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Divider,
  ActivityIndicator,
  Button,
  Surface,
  Chip,
} from 'react-native-paper';
import { checkHealth, getCollectionInfo } from '../services/api';

export default function HomeScreen() {
  const [health, setHealth] = useState(null);
  const [collectionInfo, setCollectionInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const [healthData, infoData] = await Promise.all([
        checkHealth(),
        getCollectionInfo(),
      ]);
      setHealth(healthData);
      setCollectionInfo(infoData);
    } catch (error) {
      console.error('Error loading data:', error);
      Alert.alert(
        'Connection Error',
        'Unable to connect to the backend server. Please make sure:\n\n' +
        '1. The backend is running (run_api.sh)\n' +
        '2. The API_BASE_URL in services/api.js is correct\n' +
        '3. Your device is on the same network'
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" />
        <Paragraph style={styles.loadingText}>
          Connecting to backend...
        </Paragraph>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <Surface style={styles.surface} elevation={2}>
        <Title style={styles.title}>🔎 Semantic Image Search</Title>
        <Paragraph style={styles.subtitle}>
          AI-powered image search using CLIP embeddings
        </Paragraph>
      </Surface>

      {health && (
        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.headerRow}>
              <Title style={styles.cardTitle}>🏥 Health Status</Title>
              <Chip
                icon="check-circle"
                style={styles.statusChip}
                textStyle={{ color: '#fff' }}
              >
                {health.status}
              </Chip>
            </View>
            <Divider style={styles.divider} />
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Service:</Paragraph>
              <Paragraph style={styles.value}>{health.service}</Paragraph>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Collection:</Paragraph>
              <Paragraph style={styles.value}>{health.collection}</Paragraph>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Endpoint:</Paragraph>
              <Paragraph style={styles.valueSmall} numberOfLines={2}>
                {health.cluster_endpoint}
              </Paragraph>
            </View>
          </Card.Content>
        </Card>
      )}

      {collectionInfo && (
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>📊 Collection Info</Title>
            <Divider style={styles.divider} />
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Images Indexed:</Paragraph>
              <Chip style={styles.countChip}>
                {collectionInfo.points_count}
              </Chip>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Vector Size:</Paragraph>
              <Paragraph style={styles.value}>
                {collectionInfo.config?.vector_size || 'N/A'}
              </Paragraph>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Distance Metric:</Paragraph>
              <Paragraph style={styles.value}>
                {collectionInfo.config?.distance || 'N/A'}
              </Paragraph>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.label}>Status:</Paragraph>
              <Chip
                icon="database"
                mode="outlined"
                style={styles.statusOutlineChip}
              >
                {collectionInfo.status}
              </Chip>
            </View>
          </Card.Content>
        </Card>
      )}

      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.cardTitle}>🚀 Getting Started</Title>
          <Divider style={styles.divider} />
          <View style={styles.featureItem}>
            <Paragraph style={styles.featureTitle}>🔍 Text Search</Paragraph>
            <Paragraph style={styles.featureDesc}>
              Search for images using natural language queries like "yellow flowers" or "wild animals"
            </Paragraph>
          </View>
          <View style={styles.featureItem}>
            <Paragraph style={styles.featureTitle}>📷 Image Search</Paragraph>
            <Paragraph style={styles.featureDesc}>
              Upload an image or take a photo to find visually similar images
            </Paragraph>
          </View>
          <View style={styles.featureItem}>
            <Paragraph style={styles.featureTitle}>🏷️ Category Filters</Paragraph>
            <Paragraph style={styles.featureDesc}>
              Filter results by categories like flower, animal, furniture, etc.
            </Paragraph>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.cardTitle}>⚙️ Configuration</Title>
          <Divider style={styles.divider} />
          <Paragraph style={styles.configText}>
            Backend URL: Check services/api.js
          </Paragraph>
          <Button
            mode="outlined"
            onPress={onRefresh}
            style={styles.refreshButton}
            icon="refresh"
          >
            Refresh Connection
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    marginTop: 16,
    color: '#666',
  },
  surface: {
    margin: 16,
    padding: 20,
    borderRadius: 12,
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    color: '#666',
    textAlign: 'center',
  },
  card: {
    margin: 16,
    marginTop: 0,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 8,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  statusChip: {
    backgroundColor: '#4caf50',
  },
  divider: {
    marginVertical: 12,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
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
  valueSmall: {
    flex: 1,
    fontSize: 12,
    color: '#666',
  },
  countChip: {
    backgroundColor: '#e3f2fd',
  },
  statusOutlineChip: {
    height: 28,
  },
  featureItem: {
    marginBottom: 16,
  },
  featureTitle: {
    fontWeight: 'bold',
    fontSize: 16,
    marginBottom: 4,
  },
  featureDesc: {
    color: '#666',
    fontSize: 14,
  },
  configText: {
    color: '#666',
    marginBottom: 12,
  },
  refreshButton: {
    marginTop: 8,
  },
});
