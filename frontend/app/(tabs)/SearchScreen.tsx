import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
} from 'react-native';
import { useAuth } from '../_layout';
import styles from '../styles';
import { useRouter } from 'expo-router';

export default function SearchScreen() {
  const { user, loading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (authLoading) return;

    const fetchUsers = async () => {
      try {
        const res = await fetch('http://localhost:5000/search', {
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Failed to load users');
        const data = await res.json();
        setUsers(data);
      } catch (err) {
        Alert.alert('Error', err instanceof Error ? err.message : 'Unexpected error loading users');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [authLoading]);

  if (loading || authLoading) {
    return (
      <View style={styles.outerContainer}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 20 }}>
      <Text style={styles.screenTitle}>Search Users</Text>

      {users.map((u, idx) => (
        <View
          key={idx}
          style={[
            styles.searchCard,
            {
              flexDirection: 'row',
              justifyContent: 'space-between',
              alignItems: 'center',
            },
          ]}
        >
          <Text style={styles.searchUserText} numberOfLines={2} ellipsizeMode="tail">
            {u.first_name} {u.last_name} | {u.graduation_year || '-'} | {u.major || '-'} |{' '}
            {(u.interests || []).join(', ') || '-'} | {(u.hobbies || []).join(', ') || '-'}
          </Text>

          <View style={{ flexDirection: 'row' }}>
            <TouchableOpacity
              style={[styles.searchMessageButton, { marginRight: 10 }]}
              onPress={() =>
                router.push({
                  pathname: '../ViewBioScreen',
                  params: { userId: u.id.toString() },
                })
              }
            >
              <Text style={styles.searchMessageButtonText}>View Bio</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.searchMessageButton}
              onPress={() =>
                router.push({
                  pathname: '../MessageScreen',
                  params: {
                    userId: u.id,
                    userName: `${u.first_name} ${u.last_name}`,
                  },
                })
              }
            >
              <Text style={styles.searchMessageButtonText}>Message</Text>
            </TouchableOpacity>
          </View>
        </View>
      ))}
    </ScrollView>
  );
}
